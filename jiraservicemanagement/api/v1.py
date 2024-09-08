from atlassian.rest_client import AtlassianRestAPI

class Assets(AtlassianRestAPI):
    """
    JIRA ServiceManagement Assets API object
    """

    def __init__(self, workspaceId, auth):
        self.workspaceId = workspaceId
        super().__init__(**auth)

    def _workspaceUrl(self):
        return f"gateway/api/jsm/assets/workspace/{self.workspaceId}/v1"
    
    def get_object(self, objectId):
        return self.get(self._workspaceUrl() + f"/object/{objectId}", headers=self.experimental_headers)

    def get_object_attributes(self, objectId):
        return self.get(self._workspaceUrl() + f"/object/{objectId}/attributes", headers=self.experimental_headers)

    def get_object_history(self, objectId):
        return self.get(self._workspaceUrl() + f"/object/{objectId}/history", headers=self.experimental_headers)

    def get_object_reference_info(self, objectId):
        return self.get(self._workspaceUrl() + f"/object/{objectId}/referenceinfo", headers=self.experimental_headers)

    def get_object_connected_tickets(self, objectId):
        return self.get(self._workspaceUrl() + f"/objectconnectedtickets/{objectId}/tickets", headers=self.experimental_headers)

    def post_object_aql(self, query):
        return self.post(self._workspaceUrl() + "/object/aql", json={ "qlQuery": query }, headers=self.experimental_headers)
    
    def post_object_navlist_aql(self, query):
        return self.post(self._workspaceUrl() + "/object/navlist/aql", json={ "qlQuery": query }, headers=self.experimental_headers)
    
    def list_object_schema(self):
        return self.get(self._workspaceUrl() + "/objectschema/list", headers=self.experimental_headers)

    def get_object_schema(self, objectSchemaId):
        return self.get(self._workspaceUrl() + f"/objectschema/{objectSchemaId}", headers=self.experimental_headers)

    def get_object_schema_attributes(self, objectSchemaId):
        return self.get(self._workspaceUrl() + f"/objectschema/{objectSchemaId}/attributes", headers=self.experimental_headers)

    def get_object_schema_objecttypes(self, objectSchemaId, flat=False):
        url = self._workspaceUrl() + f"/objectschema/{objectSchemaId}/objecttypes"
        if flat:
            url += "/flat"
        return self.get(url, headers=self.experimental_headers)
        
    def get_object_type(self, objectTypeId):
        return self.get(self._workspaceUrl() + f"/objecttype/{objectTypeId}", headers=self.experimental_headers)
    

    def get_object_type_attributes(self, objectTypeId):
        return self.get(self._workspaceUrl() + f"/objecttype/{objectTypeId}/attributes", headers=self.experimental_headers)

    def list_config_status_type(self):
        return self.get(self._workspaceUrl() + "/config/statustype", headers=self.experimental_headers)
    
    def get_config_status_type(self, statusTypeId):
        return self.get(self._workspaceUrl() + f"/config/statustype/{statusTypeId}", headers=self.experimental_headers)
    

