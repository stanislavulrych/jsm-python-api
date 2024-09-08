from atlassian.rest_client import AtlassianRestAPI

class Assets(AtlassianRestAPI):
    """
    JIRA ServiceManagement Assets API object
    """

    def __init__(self, workspaceId, auth):
        args = { **auth, **{ "url": auth['url'] + f"gateway/api/jsm/assets/workspace/{workspaceId}/v1" } }
        super().__init__(**args)

    def get_object(self, objectId):
        return self.get(f"/object/{objectId}", headers=self.experimental_headers)

    def get_object_attributes(self, objectId):
        return self.get(f"/object/{objectId}/attributes", headers=self.experimental_headers)

    def get_object_history(self, objectId):
        return self.get(f"/object/{objectId}/history", headers=self.experimental_headers)

    def get_object_reference_info(self, objectId):
        return self.get(f"/object/{objectId}/referenceinfo", headers=self.experimental_headers)

    def get_object_connected_tickets(self, objectId):
        return self.get(f"/objectconnectedtickets/{objectId}/tickets", headers=self.experimental_headers)

    def post_object_aql(self, query):
        return self.post("/object/aql", json={ "qlQuery": query }, headers=self.experimental_headers)
    
    def post_object_navlist_aql(self, query):
        return self.post("/object/navlist/aql", json={ "qlQuery": query }, headers=self.experimental_headers)
    
    def list_object_schema(self):
        return self.get("/objectschema/list", headers=self.experimental_headers)

    def get_object_schema(self, objectSchemaId):
        return self.get(f"/objectschema/{objectSchemaId}", headers=self.experimental_headers)

    def get_object_schema_attributes(self, objectSchemaId):
        return self.get(f"/objectschema/{objectSchemaId}/attributes", headers=self.experimental_headers)

    def get_object_schema_objecttypes(self, objectSchemaId, flat=False):
        url = f"/objectschema/{objectSchemaId}/objecttypes"
        if flat:
            url += "/flat"
        return self.get(url, headers=self.experimental_headers)
        
    def get_object_type(self, objectTypeId):
        return self.get(f"/objecttype/{objectTypeId}", headers=self.experimental_headers)
    

    def get_object_type_attributes(self, objectTypeId):
        return self.get(f"/objecttype/{objectTypeId}/attributes", headers=self.experimental_headers)

    def list_config_status_type(self):
        return self.get("/config/statustype", headers=self.experimental_headers)
    
    def get_config_status_type(self, statusTypeId):
        return self.get(f"/config/statustype/{statusTypeId}", headers=self.experimental_headers)
    

