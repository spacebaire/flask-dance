from __future__ import unicode_literals

from flask_dance.consumer import OAuth2ConsumerBlueprint
from functools import partial
from flask.globals import LocalProxy, _lookup_app_object
try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack


__maintainer__ = "David Baumgold <david@davidbaumgold.com>"


def make_github_blueprint(client_id=None, client_secret=None, scope=None,
                          redirect_url=None, redirect_to=None,
                          login_url=None, authorized_url=None,
                          session_class=None):
    """
    Make a blueprint for authenticating with Github using OAuth 2. This requires
    a client ID and client secret from Github. You should either pass them to
    this constructor, or make sure that your Flask application config defines
    them, using the variables GITHUB_OAUTH_CLIENT_ID and GITHUB_OAUTH_CLIENT_SECRET.

    Args:
        client_id (str): The client ID for your application on Github.
        client_secret (str): The client secret for your application on Github
        scope (str, optional): comma-separated list of scopes for the OAuth token
        redirect_url (str): the URL to redirect to after the authentication
            dance is complete
        redirect_to (str): if ``redirect_url`` is not defined, the name of the
            view to redirect to after the authentication dance is complete.
            The actual URL will be determined by :func:`flask.url_for`
        login_url (str, optional): the URL path for the ``login`` view.
            Defaults to ``/github``
        authorized_url (str, optional): the URL path for the ``authorized`` view.
            Defaults to ``/github/authorized``.
        session_class (class, optional): The class to use for creating a
            Requests session. Defaults to
            :class:`~flask_dance.consumer.oauth2.OAuth2SessionWithBaseURL`.

    :rtype: :class:`~flask_dance.consumer.OAuth2ConsumerBlueprint`
    :returns: A :ref:`blueprint <flask:blueprints>` to attach to your Flask app.
    """
    github_bp = OAuth2ConsumerBlueprint("github", __name__,
        client_id=client_id,
        client_secret=client_secret,
        scope=scope,
        base_url="https://api.github.com/",
        authorization_url="https://github.com/login/oauth/authorize",
        token_url="https://github.com/login/oauth/access_token",
        redirect_url=redirect_url,
        redirect_to=redirect_to,
        login_url=login_url,
        authorized_url=authorized_url,
        session_class=session_class,
    )
    github_bp.from_config["client_id"] = "GITHUB_OAUTH_CLIENT_ID"
    github_bp.from_config["client_secret"] = "GITHUB_OAUTH_CLIENT_SECRET"

    @github_bp.before_app_request
    def set_applocal_session():
        ctx = stack.top
        ctx.github_oauth = github_bp.session

    return github_bp

github = LocalProxy(partial(_lookup_app_object, "github_oauth"))