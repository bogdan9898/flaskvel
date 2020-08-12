from distutils.core import setup

setup(
	name = 'flaskvel',         # How you named your package folder (MyLib)
	packages = ['flaskvel'],   # Chose the same as "name"
	version = '0.7.1',      # Start with a small number and increase it with every change you make
	license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
	description = 'A small package that provides a convenient method to validate incoming HTTP requests with a variety of powerful validation rules, highly customizable and heavily influenced by Laravel.',   # Give a short description about your library
	author = 'Bogdan I.',                   # Type in your name
	author_email = 'bogdan.istoc98@gmail.com',      # Type in your E-Mail
	url = 'https://github.com/bogdan9898/flaskvel',   # Provide either the link to your github or to your website
	download_url = 'https://github.com/bogdan9898/flaskvel/archive/v0.7.1-alpha.tar.gz',    # I explain this later on
	keywords = ['flask', 'http', 'validator', 'request validator'],   # Keywords that define your package best
	install_requires=[            # I get to this in a second
		'flask',
		'python-dateutil',
		'pytz',
		'requests',
		'Pillow',
	],
	classifiers=[
		'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
		'Intended Audience :: Developers',      # Define that your audience are developers
		'Topic :: Software Development :: Build Tools',
		'License :: OSI Approved :: MIT License',   # Again, pick a license
		'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
		'Programming Language :: Python :: 3.8',
	],
)