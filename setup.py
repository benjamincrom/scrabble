from setuptools import setup

setup(name='scrabble',
      version='1.2',
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
      zip_safe=False,
      classifiers=[
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Topic :: Games/Entertainment :: Board Games',
          'Topic :: Games/Entertainment :: Puzzle Games',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules']
)
