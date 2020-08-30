from setuptools import setup, find_packages

long_description = None
with open("README.md", "r") as file:
    long_description = file.read()

setup(
	name = 'flaskvel',
	packages = find_packages(),
	version = '1.0',
	license='MIT',
	description = 'A small package for validating incoming HTTP requests',
	long_description=long_description,
    long_description_content_type="text/markdown",
	author = 'Bogdan Istoc',
	author_email = 'bogdan.istoc98@gmail.com',
	url = 'https://github.com/bogdan9898/flaskvel',
	download_url = 'https://github.com/bogdan9898/flaskvel/archive/v1.0.tar.gz',
	keywords = ['flask', 'http', 'validator', 'request validator', 'http validator'],
	install_requires=[
		'flask',
		'python-dateutil',
		'pytz',
		'requests',
		'Pillow',
	],
	classifiers=[
		'Development Status :: 3 - Alpha', # 3 - Alpha, 4 - Beta or 5 - Production/Stable
		'Intended Audience :: Developers',
		'Topic :: Software Development :: Build Tools',
		'License :: OSI Approved :: MIT License', 
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
		'Programming Language :: Python :: 3.8',
	],
	python_requires='>=3.6'
)