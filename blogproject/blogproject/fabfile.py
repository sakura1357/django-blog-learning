from fabric.api import env, run
from fabric.operations import sudo

GIT_REPO = 'https://github.com/sakura1357/django-blog-learning.git'

env.user = 'siar'
env.password = '123456'

env.hosts = ['192.168.171.134']

env.port = '22'


def deploy():
	source_folder = '/home/siar/sites/django-blog-learning/blogproject'

	run('cd %s && git pull' % source_folder)
	run("""
		cd {} &&
		/home/siar/sites/env/bin/pip3 install -r requirements.txt &&
		/home/siar/sites/env/bin/python3 manage.py collectstatic --noinput &&
		/home/siar/sites/env/bin/python3 manage.py migrate
	""".format(source_folder))
	sudo('restart siar')
	sudo('service nginx reload')

