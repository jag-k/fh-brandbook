from bottle import HTTPResponse, static_file, run
from router import route, template, app
import config


@route("/<file:path>")
def static(file):
    f = static_file(file, "./public")
    if f.status_code == 404:
        return HTTPResponse(
            body=template(
                "error",
                template_title="404",
            ),
            status=404
        )
    if not config.DEBUG:
        f.set_header("Cache-Control", "public, max-age=%d" % config.RESOURCE_CACHE)
    return f


if __name__ == '__main__':
    run(app=app, host="0.0.0.0", port=8000, quiet=False, reloader=True, debug=config.DEBUG)
