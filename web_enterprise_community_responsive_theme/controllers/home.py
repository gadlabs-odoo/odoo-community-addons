# Copyright Badirra / Mahmoud Salheen - All rights reserved.
# Author: Mahmoud Salheen
# License OPL-1 (Odoo Proprietary License v1.0) - see the LICENSE file.

from odoo.addons.web.controllers import home as web_home
from odoo.http import request, route

COOKIE = "color_scheme"


class Home(web_home.Home):
    @route()
    def web_login(self, redirect=None, **kw):
        """Restore the saved colour scheme as part of signing in.

        This is what stops dark mode from "resetting" after a logout. The
        sequence that broke was:

          1. user turns dark mode on   -> cookie set, preference saved
          2. user logs out             -> _post_logout clears the cookie
          3. user logs back in         -> no cookie, so the page renders
                                          light, even though the saved
                                          preference still says dark
          4. any refresh               -> now correct

        Step 3 is unavoidable if the cookie is only written on the way out
        of the webclient route: Odoo 18's web.layout picks the stylesheet
        by reading the cookie *while rendering*, so a cookie set on that
        same response arrives one page too late.

        Setting it here instead fixes the ordering. A successful login ends
        in a redirect to the webclient, so the cookie set on that redirect
        is already in the browser when it requests the next page - the
        first render is correct and there is nothing to refresh.

        The preference is read for request.session.uid explicitly rather
        than from request.env.user: authentication has only just happened
        and the environment can still be carrying the public user, which
        would resolve the wrong person's setting.
        """
        response = super().web_login(redirect=redirect, **kw)
        if request.params.get("login_success") and request.session.uid:
            user = request.env["res.users"].sudo().browse(request.session.uid)
            response.set_cookie(
                COOKIE,
                request.env["ir.http"]._badirra_color_scheme(user=user),
            )
        return response

    @route()
    def web_client(self, s_action=None, **kw):
        """Keep the colour-scheme cookie in step with the saved preference.

        web_login above covers the common path, but the cookie can still
        drift from the stored preference: the user may have changed it in
        another browser, or arrived on an existing session whose cookie was
        cleared. Rewriting it on each webclient load restores it from the
        server rather than leaving the browser stuck on light.

        Bare @route() re-uses the parent's routing configuration (paths,
        auth, readonly) rather than restating it, so this stays correct if
        Odoo changes any of that.
        """
        response = super().web_client(s_action, **kw)
        if getattr(response, "status_code", None) == 200:
            response.set_cookie(
                COOKIE,
                request.env["ir.http"]._badirra_color_scheme(),
            )
        return response
