import request from "../HttpCommon.js";

class ModuleApi {
  getProModule(data) {
    return request.get("/api/modules/tree", data);
  }

  createModules(data) {
    return request.post("/api/modules/", data);
  }

  deleteModules(mid) {
    return request.delete("/api/modules/" + mid + "/");
  }

  getModuleCases(mid) {
    return request.get("/api/modules/" + mid + "/cases");
  }

  updateProject(id, data) {
    return request.put("/api/projects/" + id + "/", data);
  }
}

export default new ModuleApi();
