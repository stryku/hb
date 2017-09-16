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

    def set_password(self, passw):
        self.password = passw

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
        self.git.checkout('HEAD', b=branch)

    def push_all(self):
        command = ('git push https://stryku-bot%s:@github.com/stryku/%s --all' % self.password, self.repo_name)
        utils.run_process_split(command, cwd=self.repo_dir)

    def repo_dir(self):
        return self.repo_dir
