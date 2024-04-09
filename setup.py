from setuptools import setup, find_packages

setup(zip_safe = True,
      include_package_data = True,
      install_requires=["python-dateutil >= 2.5.0; python_version < '3.10'",
                        "python-dateutil >= 2.7.0; python_version >= '3.10'",
                        "pytz", 'six'],
      platforms = ["any"],
      packages = find_packages(),
      test_suite="tests",
      )
