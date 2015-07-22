
from django import http
from django.http import HttpResponseRedirect
from django.views.generic.simple import direct_to_template

try:
    from openid.consumer import consumer
    from openid.consumer.discover import DiscoveryFailure, OPENID_IDP_2_0_TYPE, OPENID_2_0_TYPE, OPENID_1_1_TYPE, OPENID_1_0_TYPE, OpenIDServiceEndpoint
    from openid.extensions import ax, pape, sreg
    from openid.yadis.constants import YADIS_HEADER_NAME, YADIS_CONTENT_TYPE
    from openid.yadis.manager import Discovery
    from openid.server.trustroot import RP_RETURN_TO_URL_TYPE
except:
    print "yum install python-mojeid"

import util

from apps.auth.views import create_profil_from_ipenid, index

SERVICE_NS = [
    OPENID_IDP_2_0_TYPE,
    OPENID_2_0_TYPE,
    OPENID_1_1_TYPE,
    OPENID_1_0_TYPE,
]

# include 1.x OpenID server service types
OpenIDServiceEndpoint.openid_type_uris = SERVICE_NS

SREG_ATTRIBUTES = sreg.data_fields.keys()

AX_ATTRIBUTES = [
    u'http://axschema.org/namePerson/first',
  u'http://axschema.org/namePerson/last',
  u'http://axschema.org/contact/email',
]

"""
# http://www.axschema.org/types/
AX_ATTRIBUTES = [
    'http://axschema.org/birthDate',
    'http://axschema.org/company/name',
    'http://axschema.org/contact/city/home',
    'http://axschema.org/contact/country/home',
    'http://axschema.org/contact/email',
    'http://axschema.org/contact/IM/ICQ',
    'http://axschema.org/contact/IM/Jabber',
    'http://axschema.org/contact/IM/Skype',
    'http://axschema.org/contact/phone/business',
    'http://axschema.org/contact/phone/cell',
    'http://axschema.org/contact/phone/default',
    'http://axschema.org/contact/phone/fax',
    'http://axschema.org/contact/phone/home',
    'http://axschema.org/contact/postalAddressAdditional/home',
    'http://axschema.org/contact/postalAddress/home',
    'http://axschema.org/contact/postalCode/home',
    'http://axschema.org/contact/state/home',
    'http://axschema.org/contact/web/blog',
    'http://axschema.org/contact/web/default',
    'http://axschema.org/namePerson',
    'http://axschema.org/namePerson/first',
    'http://axschema.org/namePerson/friendly',
    'http://axschema.org/namePerson/last',
    'http://specs.nic.cz/attr/addr/bill/cc',
    'http://specs.nic.cz/attr/addr/bill/city',
    'http://specs.nic.cz/attr/addr/bill/pc',
    'http://specs.nic.cz/attr/addr/bill/sp',
    'http://specs.nic.cz/attr/addr/bill/street',
    'http://specs.nic.cz/attr/addr/bill/street2',
    'http://specs.nic.cz/attr/addr/bill/street3',
    'http://specs.nic.cz/attr/addr/mail/cc',
    'http://specs.nic.cz/attr/addr/mail/city',
    'http://specs.nic.cz/attr/addr/mail/pc',
    'http://specs.nic.cz/attr/addr/mail/sp',
    'http://specs.nic.cz/attr/addr/mail/street',
    'http://specs.nic.cz/attr/addr/mail/street2',
    'http://specs.nic.cz/attr/addr/mail/street3',
    'http://specs.nic.cz/attr/addr/main/cc',
    'http://specs.nic.cz/attr/addr/main/city',
    'http://specs.nic.cz/attr/addr/main/pc',
    'http://specs.nic.cz/attr/addr/main/sp',
    'http://specs.nic.cz/attr/addr/main/street',
    'http://specs.nic.cz/attr/addr/main/street2',
    'http://specs.nic.cz/attr/addr/main/street3',
    'http://specs.nic.cz/attr/addr/ship/cc',
    'http://specs.nic.cz/attr/addr/ship/city',
    'http://specs.nic.cz/attr/addr/ship/pc',
    'http://specs.nic.cz/attr/addr/ship/sp',
    'http://specs.nic.cz/attr/addr/ship/street',
    'http://specs.nic.cz/attr/addr/ship/street2',
    'http://specs.nic.cz/attr/addr/ship/street3',
    'http://specs.nic.cz/attr/contact/adult',
    'http://specs.nic.cz/attr/contact/ident/card',
    'http://specs.nic.cz/attr/contact/ident/dob',
    'http://specs.nic.cz/attr/contact/ident/pass',
    'http://specs.nic.cz/attr/contact/ident/ssn',
    'http://specs.nic.cz/attr/contact/ident/type',
    'http://specs.nic.cz/attr/contact/ident/vat_id',
    'http://specs.nic.cz/attr/contact/image',
    'http://specs.nic.cz/attr/contact/name',
    'http://specs.nic.cz/attr/contact/name/first',
    'http://specs.nic.cz/attr/contact/name/last',
    'http://specs.nic.cz/attr/contact/nickname',
    'http://specs.nic.cz/attr/contact/org',
    'http://specs.nic.cz/attr/contact/valid',
    'http://specs.nic.cz/attr/contact/vat',
    'http://specs.nic.cz/attr/email/main',
    'http://specs.nic.cz/attr/email/next',
    'http://specs.nic.cz/attr/email/notify',
    'http://specs.nic.cz/attr/im/google_talk',
    'http://specs.nic.cz/attr/im/icq',
    'http://specs.nic.cz/attr/im/jabber',
    'http://specs.nic.cz/attr/im/skype',
    'http://specs.nic.cz/attr/im/windows_live',
    'http://specs.nic.cz/attr/phone/fax',
    'http://specs.nic.cz/attr/phone/home',
    'http://specs.nic.cz/attr/phone/main',
    'http://specs.nic.cz/attr/phone/mobile',
    'http://specs.nic.cz/attr/phone/work',
    'http://specs.nic.cz/attr/url/blog',
    'http://specs.nic.cz/attr/url/facebook',
    'http://specs.nic.cz/attr/url/linkedin',
    'http://specs.nic.cz/attr/url/main',
    'http://specs.nic.cz/attr/url/personal',
    'http://specs.nic.cz/attr/url/rss',
    'http://specs.nic.cz/attr/url/twitter',
    'http://specs.nic.cz/attr/url/work',
]
"""


PAPE_POLICIES = [
    'AUTH_PHISHING_RESISTANT',
    'AUTH_MULTI_FACTOR',
    'AUTH_MULTI_FACTOR_PHYSICAL',
]

# List of (name, uri) for use in generating the request form.
POLICY_PAIRS = [(p, getattr(pape, p))
                for p in PAPE_POLICIES]


def getOpenIDStore():
    """
    Return an OpenID store object fit for the currently-chosen
    database backend, if any.
    """
    return util.getOpenIDStore('/tmp/djopenid_c_store', 'c_')


def getConsumer(request):
    """
    Get a Consumer object to perform OpenID authentication.
    """
    return consumer.Consumer(request.session, getOpenIDStore())


def renderIndexPage(request, **template_args):
    template_args['ns'] = SERVICE_NS
    template_args['sreg'] = SREG_ATTRIBUTES
    template_args['ax'] = AX_ATTRIBUTES
    template_args['consumer_url'] = util.getViewURL(request, startOpenID)
    template_args['pape_policies'] = POLICY_PAIRS

    response = direct_to_template(
        request, 'login.html', template_args)
    response[YADIS_HEADER_NAME] = util.getViewURL(request, rpXRDS)
    return response


def startOpenID(request):
    """
    Start the OpenID authentication process.  Renders an
    authentication form and accepts its POST.

    * Renders an error message if OpenID cannot be initiated

    * Requests some Simple Registration data using the OpenID
      library's Simple Registration machinery

    * Generates the appropriate trust root and return URL values for
      this application (tweak where appropriate)

    * Generates the appropriate redirect based on the OpenID protocol
      version.
    """
    if request.POST:
        # Start OpenID authentication (mojeid url)
        openid_url = request.POST['openid_identifier']
        c = getConsumer(request)
        error = None

        if request.session.has_key(Discovery.PREFIX + c.session_key_prefix):
            del request.session[Discovery.PREFIX + c.session_key_prefix]

        if not request.POST.has_key('ns'):
            OpenIDServiceEndpoint.openid_type_uris = SERVICE_NS
        else:
            OpenIDServiceEndpoint.openid_type_uris = request.POST.getlist('ns')

        try:
            auth_request = c.begin(openid_url)
        except DiscoveryFailure, e:
            # Some other protocol-level failure occurred.
            error = "OpenID discovery error: %s" % (str(e),)

        if error:
            # Render the page with an error.
            return renderIndexPage(request, error=error)

        # Add Simple Registration request information.  Some fields
        # are optional, some are required.  It's possible that the
        # server doesn't support sreg or won't return any of the
        # fields.
        if request.POST.has_key('sreg'):
            sreg_request = sreg.SRegRequest(
                optional=[], required=request.POST.getlist('sreg'))
            auth_request.addExtension(sreg_request)

        if True:  # request.POST.has_key('ax'):
            # Add Attribute Exchange request information.
            ax_request = ax.FetchRequest()
            # XXX - uses myOpenID-compatible schema values, which are
            # not those listed at axschema.org.
            # for uri in request.POST.getlist('ax'):
            for uri in AX_ATTRIBUTES:
                ax_request.add(
                    ax.AttrInfo(uri, required=True))
            auth_request.addExtension(ax_request)

        # Add PAPE request information.  We'll ask for
        # phishing-resistant auth and display any policies we get in
        # the response.
        requested_policies = []
        policy_prefix = 'policy_'
        for k, v in request.POST.iteritems():
            # print k,v
            if k.startswith(policy_prefix):
                policy_attr = k[len(policy_prefix):]
                if policy_attr in PAPE_POLICIES:
                    requested_policies.append(getattr(pape, policy_attr))

        print requested_policies
        if requested_policies:
            pape_request = pape.Request(requested_policies)
            auth_request.addExtension(pape_request)

        # Compute the trust root and return URL values to build the
        # redirect information.
        trust_root = util.getViewURL(request, startOpenID)
        return_to = util.getViewURL(request, finishOpenID)

        # Send the browser to the server either by sending a redirect
        # URL or by generating a POST form.
        if auth_request.shouldSendRedirect():
            url = auth_request.redirectURL(trust_root, return_to)
            return HttpResponseRedirect(url)
        else:
            # Beware: this renders a template whose content is a form
            # and some javascript to submit it upon page load.  Non-JS
            # users will have to click the form submit button to
            # initiate OpenID authentication.
            form_id = 'openid_message'
            form_html = auth_request.formMarkup(trust_root, return_to,
                                                False, {'id': form_id})
            return direct_to_template(
                request, 'consumer/request_form.html', {'html': form_html})

    return renderIndexPage(request)
    # return index(request)


def finishOpenID(request):
    """
    Finish the OpenID authentication process.  Invoke the OpenID
    library with the response from the OpenID server and render a page
    detailing the result.
    """
    result = {}

    # Because the object containing the query parameters is a
    # MultiValueDict and the OpenID library doesn't allow that, we'll
    # convert it to a normal dict.

    # OpenID 2 can send arguments as either POST body or GET query
    # parameters.
    request_args = util.normalDict(request.GET)
    if request.method == 'POST':
        request_args.update(util.normalDict(request.POST))

    if request_args:
        c = getConsumer(request)

        # Get a response object indicating the result of the OpenID
        # protocol.
        return_to = util.getViewURL(request, finishOpenID)
        response = c.complete(request_args, return_to)

        # Get a Simple Registration response object if response
        # information was included in the OpenID response.
        sreg_response = {}
        ax_items = {}
        if response.status == consumer.SUCCESS:
            sreg_response = sreg.SRegResponse.fromSuccessResponse(response)

            ax_response = ax.FetchResponse.fromSuccessResponse(response)
            if ax_response:
                ax_items = ax_response.data

        # Get a PAPE response object if response information was
        # included in the OpenID response.
        pape_response = None
        if response.status == consumer.SUCCESS:
            pape_response = pape.Response.fromSuccessResponse(response)

            if not pape_response.auth_policies:
                pape_response = None

        # Map different consumer status codes to template contexts.
        results = {
            consumer.CANCEL:
            {'message': 'OpenID authentication cancelled.'},

            consumer.FAILURE:
            {'error': 'OpenID authentication failed.'},

            consumer.SUCCESS:
            {'url': response.getDisplayIdentifier(),
             'sreg_response': sreg_response and sreg_response.iteritems(),
             'ax_response': ax_items.items(),
             'pape': pape_response}
        }

        result = results[response.status]

        print result
        if not result.has_key("error"):
            data_array = [it[1][0] for it in result["ax_response"]]
            data = {
                "login": None,
                "openid": result["url"],
                "first_name": data_array[0],
                "last_name": data_array[1],
                "email": data_array[2],
            }
            return create_profil_from_ipenid(request, data)

        if isinstance(response, consumer.FailureResponse):
            # In a real application, this information should be
            # written to a log for debugging/tracking OpenID
            # authentication failures. In general, the messages are
            # not user-friendly, but intended for developers.
            result['failure_reason'] = response.message

    return renderIndexPage(request, **result)


def rpXRDS(request):
    """
    Return a relying party verification XRDS document
    """
    return util.renderXRDS(
        request,
        [RP_RETURN_TO_URL_TYPE],
        [util.getViewURL(request, finishOpenID)])
