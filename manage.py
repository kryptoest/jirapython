# This script shows how to connect to a JIRA instance with a
# username and password over HTTP BASIC authentication.

from jira.client import JIRA
serv_options = {
    'server': 'http://188.226.200.198:8899'
}

key_cert_data = None
with open(key_cert, 'r') as key_cert_file:
    key_cert_data = key_cert_file.read()

oauth_dict = {
    'access_token': 'd87f3hajglkjh89a97f8',
    'access_token_secret': 'a9f8ag0ehaljkhgeds90',
    'consumer_key': 'jira-oauth-consumer',
    'key_cert': mykey.pem
}

# By default, the client will connect to a JIRA instance started from the Atlassian Plugin SDK.
# See https://developer.atlassian.com/display/DOCS/Installing+the+Atlassian+Plugin+SDK for details.
jira = JIRA(options=serv_options,oauth=oauth_dict)    # a username/password tuple

# Get the mutable application properties for this server (requires jira-system-administrators permission)
props = jira.application_properties()

def reindex(self, force=True, background=True):
        """
        Start jira re-indexing. Returns True if reindexing is in progress or not needed, or False.

        If you call reindex() without any parameters it will perform a backfround reindex only if Jira thinks it should do it.

        :param force: reindex even if Jira doesn'tt say this is needed, False by default.
        :param background: reindex inde background, slower but does not impact the users, defaults to True.
        """
        # /secure/admin/IndexAdmin.jspa
        # /secure/admin/jira/IndexProgress.jspa?taskId=1
        if background:
            indexingStrategy = 'background'
        else:
            indexingStrategy = 'stoptheworld'

        url = self.serv_options['server'] + '/secure/admin/jira/IndexReIndex.jspa'

        r = self._session.get(url, headers=self.serv_options['headers'])
        if r.status_code == 503:
            # logging.warning("Jira returned 503, this could mean that a full reindex is in progress.")
            return 503
        # raise_on_error(r)

        if not r.content.find("To perform the re-index now, please go to the") and force is False:
            return True

        if r.content.find('All issues are being re-indexed'):
            logging.warning("Jira re-indexing is already running.")
            return True  # still reindexing is considered still a success

        if r.content.find('To perform the re-index now, please go to the') or force:
            r = self._session.post(url, headers=self.serv_options['headers'], params={"indexingStrategy": indexingStrategy, "reindex": "Re-Index"})
            # raise_on_error(r)
            if r.content.find('All issues are being re-indexed') != -1:
                return True
            else:
                logging.error("Failed to reindex jira, probably a bug.")
                return False
