from ... import profile

def main(**kwargs):
    profile.manager.currents.update(kwargs)
    profile.manager.print_status()
    log, web = profile.manager.instances('log', 'web')
    if NotImplemented in [web]:
        log.error('Unable to initialize profiles. Stop...')
    else:
        try:
            log.debug(web.format_status())
            return web.run()
        except Exception as e:
            log.error('Failed to run app. ({!s})'.format(e))
if __name__ == '__api_main__':
    main()
