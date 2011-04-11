from django.core import management

def main(settings_file, coverage_html_path, apps):
    with_coverage = False
    if coverage_html_path:
        try:
            from coverage import coverage
            with_coverage = True
        except ImportError:
            print "coverage not installed! running tests without coverage."
            coverage = None
    argv = ['test', 'test'] + list(apps)
    try:
        mod = __import__(settings_file)
        components = settings_file.split('.')
        for comp in components[1:]:
            mod = getattr(mod, comp)

    except ImportError, e:
        import sys
        sys.stderr.write("Error loading the settings module '%s': %s"
                            % (settings_file, e))
        return sys.exit(1)

    management.setup_environ(mod, settings_file)
    utility = management.ManagementUtility(argv)
    if with_coverage:
        cov = coverage(cover_pylib=False, branch=True, 
                       source=list(apps), 
                       omit=['../*migrations*','../*tests*'])
        cov.start()
    utility.execute()
    if with_coverage:
        cov.stop()
        cov.html_report(directory=coverage_html_path)
