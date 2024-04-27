import base64, json
import pandas as pd
from requests import Session
from io import StringIO

"""
Sam's notes:
- read/write large currently not used
- i don't care about the sha in my read/write routines

Additinonal methods added by Sam:
- file_exists - returns True if the file exists, False otherwise
- read_text, write_text - must be str
- read_json, write_json - must be dict or list (I don't include values alone)
- read_df, write_df - must be DataFrame
"""


class GithubContents:
    class NotFound(Exception):
        pass

    class UnknownError(Exception):
        pass

    def __init__(self, owner, repo, token, branch="main"):
        self.owner = owner
        self.repo = repo
        self.token = token
        self.session = Session()
        self.branch = branch

    def base_url(self):
        return "https://api.github.com/repos/{}/{}".format(self.owner, self.repo)

    def headers(self):
        return {"Authorization": "token {}".format(self.token)}

    def read(self, filepath):
        "Returns (file_contents_in_bytes, sha1)"
        # Try reading using content API
        content_url = "{}/contents/{}".format(self.base_url(), filepath)
        response = self.session.get(content_url, headers=self.headers())
        if response.status_code == 200:
            data = response.json()
            return base64.b64decode(data["content"]), data["sha"]
        elif response.status_code == 404:
            raise self.NotFound(filepath)
        elif response.status_code == 403:
            # It's probably too large
            if response.json()["errors"][0]["code"] != "too_large":
                raise self.UnknownError(response.content)
            else:
                return self.read_large(filepath)
        else:
            raise self.UnknownError(response.content)

    def read_large(self, filepath):
        "Returns (file_contents_in_bytes, sha1)"
        default_tree = self.session.get(
            self.base_url() + "/git/trees/{}?recursive=1".format(self.branch),
            headers=self.headers(),
        ).json()
        try:
            tree_entry = [t for t in default_tree["tree"] if t["path"] == filepath][0]
        except IndexError:
            raise self.NotFound(filepath)
        data = self.session.get(tree_entry["url"], headers=self.headers()).json()
        return base64.b64decode(data["content"]), data["sha"]

    def write(
        self, filepath, content_bytes, sha=None, commit_message="", committer=None
    ):
        if not isinstance(content_bytes, bytes):
            raise TypeError("Content_bytes must be a bytestring - better use write_text, write_json or write_df instead.")
        github_url = "{}/contents/{}".format(self.base_url(), filepath)
        payload = {
            "path": filepath,
            "content": base64.b64encode(content_bytes).decode("latin1"),
            "message": commit_message,
        }
        if sha:
            payload["sha"] = sha
        if committer:
            payload["committer"] = committer

        response = self.session.put(github_url, json=payload, headers=self.headers())
        if (
            response.status_code == 403
            and response.json()["errors"][0]["code"] == "too_large"
        ):
            return self.write_large(filepath, content_bytes, commit_message, committer)
        elif (
            sha is None
            and response.status_code == 422
            and "sha" in response.json().get("message", "")
        ):
            # Missing sha - we need to figure out the sha and try again
            _, old_sha = self.read(filepath)
            return self.write(
                filepath,
                content_bytes,
                sha=old_sha,
                commit_message=commit_message,
                committer=committer,
            )
        elif response.status_code in (201, 200):
            updated = response.json()
            return updated["content"]["sha"], updated["commit"]["sha"]
        else:
            raise self.UnknownError(
                str(response.status_code) + ":" + repr(response.content)
            )

    def write_large(self, filepath, content_bytes, commit_message="", committer=None):
        if not isinstance(content_bytes, bytes):
            raise TypeError("content_bytes must be a bytestring")
        # Create a new blob with the file contents
        created_blob = self.session.post(
            self.base_url() + "/git/blobs",
            json={
                "encoding": "base64",
                "content": base64.b64encode(content_bytes).decode("latin1"),
            },
            headers=self.headers(),
        ).json()
        # Retrieve default tree sha
        default_branch_sha = self.session.get(
            self.base_url() + "/git/trees/{}?recursive=1".format(self.branch),
            headers=self.headers(),
        ).json()["sha"]
        # Construct a new tree
        created_tree = self.session.post(
            self.base_url() + "/git/trees",
            json={
                "base_tree": default_branch_sha,
                "tree": [
                    {
                        "mode": "100644",  # file (blob),
                        "path": filepath,
                        "type": "blob",
                        "sha": created_blob["sha"],
                    }
                ],
            },
            headers=self.headers(),
        ).json()
        # Create a commit which references the new tree
        payload = {
            "message": commit_message,
            "parents": [default_branch_sha],
            "tree": created_tree["sha"],
        }
        if committer:
            payload["committer"] = committer
        created_commit = self.session.post(
            self.base_url() + "/git/commits", json=payload, headers=self.headers()
        ).json()
        # Move HEAD reference on master to the new commit
        self.session.patch(
            self.base_url() + "/git/refs/heads/{}".format(self.branch),
            json={"sha": created_commit["sha"]},
            headers=self.headers(),
        ).json()
        return created_blob["sha"], created_commit["sha"]

    def branch_exists(self):
        assert self.branch
        return (
            self.session.get(
                self.base_url() + "/git/refs/heads/{}".format(self.branch),
                headers=self.headers(),
            ).status_code
            == 200
        )
    
    # --------------- Sam's new read/write methods ---------------
    def file_exists(self, filepath):
        """
        Returns True if the file exists, False otherwise.

        Args:
        - filepath: str, the file path

        Returns:
        - bool, True if the file exists, False otherwise
        """
        try:
            self.read(filepath)
            return True
        except:
            return False


    def read_text(self, filepath):
        """
        Read text from a given filepath on github.

        Args:
        - filepath: str, the file path

        Returns:
        - str, the text
        """
        content, _ = self.read(filepath)
        return content.decode("utf-8")
    
    def write_text(self, filepath, text, commit_message):
        """
        Write text to a given filepath on github.

        Args:
        - filepath: str, the file path
        - text: str, the text to write
        - commit_message: str, the commit message
        """
        if not isinstance(text, str):
            raise TypeError("text must be a string")
        
        self.write(filepath, text.encode("utf-8"), commit_message = commit_message)

    def write_json(self, filepath, data, commit_message):
        """
        Write a json to a given filepath on github.

        Args:
        - filepath: str, the file path
        - data: dict or list, the data to write
        - commit_message: str, the commit message
        """
        if not isinstance(data, (dict, list)):
            raise TypeError("data must be a dict or list")
        
        self.write_text(filepath, json.dumps(data, indent=2), commit_message)   

    def read_json(self, filepath):
        """
        Read a json from a given filepath on github.

        Args:
        - filepath: str, the file path

        Returns:
        - dict or list, the data
        """
        return json.loads(self.read_text(filepath))
    
    def write_df(self, filepath, df, commit_message, **df_to_csv_kwargs):
        """
        Write a dataframe to a given filepath on github.

        Args:
        - filepath: str, the file path
        - df: DataFrame, the dataframe to write
        - commit_message: str, the commit message
        - **dataframe_to_csv_kwargs: additional keyword arguments to pass to DataFrame.to_csv
        """
        if not isinstance(df, pd.DataFrame, **df_to_csv_kwargs):
            raise TypeError("df must be a DataFrame")
        
        self.write_text(filepath, df.to_csv(index=False), commit_message)

    def read_df(self, filepath, **pd_read_csv_kwargs):
        """
        Read a dataframe from a given filepath on github.

        Args:
        - filepath: str, the file path
        - **read_csv_kwargs: additional keyword arguments to pass to pd.read_csv

        Returns:
        - DataFrame, the dataframe
        """
        csv_string = self.read_text(filepath)
        string_buffer = StringIO(csv_string)
        df = pd.read_csv(string_buffer, **pd_read_csv_kwargs)
        return df

    
