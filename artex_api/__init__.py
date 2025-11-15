import pymysql

# Use PyMySQL as a drop-in replacement for MySQLdb (used by mysqlclient).
# This makes Django's `django.db.backends.mysql` use PyMySQL transparently.
# Some Django checks expect mysqlclient to expose a version >= 1.4.3.
# When using PyMySQL as a drop-in, fake a compatible version string so
# Django's backend version check passes.
pymysql.__version__ = getattr(pymysql, "__version__", "1.0.0")
try:
	# If the installed pymysql version is older than 1.4.3, override to satisfy Django
	pymysql.__version__ = "1.4.3"
	# also set version_info tuple which Django's check may inspect
	pymysql.version_info = (1, 4, 3, "final", 0)
except Exception:
	pymysql.__version__ = "1.4.3"
	pymysql.version_info = (1, 4, 3, "final", 0)

# Register as MySQLdb after adjusting reported version
pymysql.install_as_MySQLdb()

