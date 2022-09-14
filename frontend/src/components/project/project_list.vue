<template>
  <div class="home">
    <div style="height: 50px; text-align: left; width: 100%">
      <el-button type="primary" @click="showDialog()">创建</el-button>
    </div>
    <el-row>
      <div v-for="(item, index) in tableData" :key="index">
        <el-col :span="7" class="project-card">
          <el-card class="box-card">
            <div slot="header" class="clearfix">
              <span>{{ item.name }} </span>
              <span style="float: right; padding: 3px 0" />
              <div style="float: right">
                <el-dropdown>
                  <span class="el-dropdown-link">
                    <i class="el-icon-setting" />
                  </span>
                  <el-dropdown-menu slot="dropdown">
                    <el-dropdown-item>
                      <el-button type="text" @click="showEdit(item.id)"
                        >编辑
                      </el-button>
                    </el-dropdown-item>
                    <el-dropdown-item>
                      <el-button type="text" @click="deleteProject(item.id)"
                        >删除
                      </el-button>
                    </el-dropdown-item>
                  </el-dropdown-menu>
                </el-dropdown>
              </div>
            </div>
            <!--              <div>-->
            <!--                {{ item.describe }}-->
            <!--              </div>-->
            <img
              :src="item.image"
              class="image"
              style="height: 235px; width: 235px"
              alt=""
            />
          </el-card>
        </el-col>
      </div>
    </el-row>
    <div style="height: 100%; text-align: right"></div>
    <div style="width: 100%; text-align: right">
      <el-pagination
        cy-data="ProjectPagination"
        background
        @current-change="handleCurrentChange"
        layout="prev, pager, next"
        :page-size="req.size"
        :total="total"
      >
      </el-pagination>
    </div>
    <!--引入子组件-->
    <projectDialog
      v-if="dialogFlag"
      @cancel="closeDiglog"
      :title="dialogTitle"
      :pid="curretProjectId"
    ></projectDialog>
  </div>
</template>

<script>
// @ is an alias to /src
import projectDialog from "./projectDialog.vue";
import ProjectApi from "../../request/project";

export default {
  name: "Project",
  components: {
    projectDialog,
  },
  data() {
    return {
      tableData: [],
      total: 50,
      dialogFlag: false,
      dialogTitle: "create",
      curretProjectId: "",
      req: {
        page: 1,
        size: 6,
      },
    };
  },
  mounted() {
    this.initProjectlist();
  },
  methods: {
    //获取项目列表接口
    async initProjectlist() {
      const resp = await ProjectApi.getProjects(this.req);
      if (resp.success === true) {
        for (let i = 0; i < resp.items.length; i++) {
          resp.items[i].image = "/static/images/" + resp.items[i].image;
        }
        this.tableData = resp.items;
        this.total = resp.total;
        this.$message.success("查询成功");
      } else {
        this.$message.error("查询失败");
      }
    },
    showEdit(id) {
      this.curretProjectId = id;
      this.dialogTitle = "edit";
      this.dialogFlag = true;
    },
    async deleteProject(id) {
      const resp = await ProjectApi.delProject(id);
      if (resp.success === true) {
        this.tableData = resp.items;
        this.total = resp.total;
        this.$message.success("删除成功");
        this.initProjectlist();
      } else {
        this.$message.error("删除失败");
      }
    },
    showDialog() {
      this.dialogTitle = "create";
      this.dialogFlag = true;
    },
    closeDiglog() {
      this.dialogFlag = false;
      this.initProjectlist();
    },
    //跳转到第几页
    handleCurrentChange(val) {
      console.log(`当前页: ${val}`);
      this.req.page = val;
      this.initProjectlist();
    },
  },
};
</script>
<style>
.box-card {
}

.project-card {
  margin-left: 15px;
  margin-right: 15px;
  margin-top: 15px;
  margin-bottom: 15px;
}
</style>
