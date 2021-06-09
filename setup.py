from setuptools import setup, find_packages

exec(open('plantseg/__version__.py').read())
setup(
    name='moebiusgol',
    version=__version__,
    packages=find_packages(),
    include_package_data=True,
    description='moebius-game-of-life.',
    author='Lorenzo Cerrone',
    url='https://github.com/lorenzocerrone/moebius-game-of-life',
    author_email='lorenzo.cerrone@iwr.uni-heidelberg.de',
)
