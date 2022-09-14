import request from "../HttpCommon.js";

class TasksApi {
  createTasks(data) {
    return request.post("/api/tasks/", data);
  }
  getTasksList(data) {
    return request.get("/api/tasks/list", data);
  }
  getTaskDetail(tid) {
    return request.get("/api/tasks/" + tid + "/");
  }
  updateTasks(tid, data) {
    return request.put("/api/tasks/" + tid + "/", data);
  }
  deleteTask(tid) {
    return request.delete("/api/tasks/" + tid + "/");
  }
  runTasks(tid) {
    return request.post("/api/tasks/" + tid + "/running");
  }
}

export default new TasksApi();
