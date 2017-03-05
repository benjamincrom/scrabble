from setuptools import setup

setup(name='scrabble',
      version='0.5',
      description='Scrabble game with move recovery and best move analysis',
      url='https://github.com/benjamincrom/scrabble',
      author='Benjamin B. Crom',
      author_email='benjamincrom@gmail.com',
      include_package_data=True,
      license='MIT',
      packages=['scrabble'],
      setup_requires=['pytest-runner'],
      scripts=['bin/recover_scrabble_game'],
      tests_require=['pytest'],
      zip_safe=False)
