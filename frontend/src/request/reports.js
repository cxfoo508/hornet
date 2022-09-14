import request from "../HttpCommon.js";

class ReportsApi {
  getReportList(data) {
    return request.get("/api/reports/list", data);
  }
  getReportDetail(rid) {
    return request.get("/api/reports/" + rid + "/");
  }
  deleteReport(rid) {
    return request.delete("/api/reports/" + rid + "/");
  }
}

export default new ReportsApi();
