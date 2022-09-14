import request from "../HttpCommon.js";

class CasesApi {
  casesDebug(data) {
    return request.post("/api/cases/debug", data);
  }

  assertCase(data) {
    return request.post("/api/cases/assert", data);
  }
  createCase(data) {
    return request.post("/api/cases/", data);
  }
  getCases(cid) {
    return request.get("/api/cases/" + cid + "/");
  }
  updateCases(uid, data) {
    return request.put("/api/cases/" + uid + "/", data);
  }
}

export default new CasesApi();
