from git import Repo
import os
import shutil
import stat
import utils
import tempfile


def on_rm_error(func, path, exc_info):
    # path contains the path of the file that couldn't be removed
    # let's just assume that it's read-only and unlink it.
    os.chmod(path, stat.S_IWRITE)
    os.unlink(path)


class StrykuBot:
    def __init__(self):
        self.password = ''
        self.gh_url = 'https://github.com/stryku/'
        self.repo_name = ''
        self.name = 'stryku-bot'
        self.email = 'strykubot@gmail.com'
        self.repo_dir = ''
        self.tmp_repo_dir = None
        self.repo = None
        self.git = None
        self.commit_prefix = '[stryku-bot]: '
        self.last_branch = ''
        file = open('strykubot.password')
        self.password = file.read().stip()
        file.close()

    def clone_repo(self, repo_name, dest='build', rm_old=True):
        if rm_old:
            if os.path.exists(dest):
                shutil.rmtree(dest, onerror=on_rm_error)

        self.repo_dir = dest
        self.repo_name = repo_name
        self.repo = Repo.clone_from(self.gh_url + self.repo_name, dest)
        self.git = self.repo.git
        self.git.checkout('dev')
        writer = self.repo.config_writer()
        writer.set_value('user', 'name', self.name)
        writer.set_value('user', 'email', self.email)
        writer.write()

    def clone_tmp_repo(self, repo_name):
        self.tmp_repo_dir = tempfile.TemporaryDirectory()
        self.clone_repo(repo_name, self.tmp_repo_dir.name, False)

    def add_all(self):
        self.git.add('--all')

    def checkout_branch(self, branch):
        self.last_branch = branch
        try:
            self.git.checkout('HEAD', b=branch)
        except Exception:
            print("Branch already exist. Remove and create a new one")
            self.git.branch('-D', branch)
            self.git.checkout('HEAD', b=branch)

    def commit(self, msg):
        self.git.commit(m=self.commit_prefix + msg)

    def push_last_branch(self):
        command = ('git push https://stryku-bot:%s@github.com/stryku/%s %s' % (self.password, self.repo_name, self.last_branch))
        print(utils.run_process_split(command, cwd=self.repo_dir))

    def get_repo_dir(self):
        return self.repo_dir
