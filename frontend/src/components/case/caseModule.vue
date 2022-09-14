<template>
  <div class="case">
    <div style="height: 100px; width: 100%">
      <el-form :inline="true">
        <el-form-item label="项目列表" style="float: left">
          <el-select
            v-model="projectValue"
            placeholder="请选择项目"
            @change="changeProject"
          >
            <el-option
              v-for="item in projectOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item style="float: right">
          <el-button type="primary" @click="createCase()" size="medium"
            >创建用例</el-button
          >
        </el-form-item>
      </el-form>
    </div>

    <el-card style="width: 20%; float: left">
      <el-button
        type="text"
        icon="el-icon-circle-plus-outline"
        @click="createRootModule"
        >根节点
      </el-button>
      <div style="margin-top: 6px">
        <el-tree
          :data="moduleDate"
          node-key="id"
          default-expand-all
          :expand-on-click-node="false"
          @node-click="nodeClick"
        >
          <span class="custom-tree-node" slot-scope="{ node, data }">
            <span style="float: left">{{ node.label }}</span>
            <span style="float: right">
              <el-button type="text" size="mini" @click="() => append(data)">
                <i class="el-icon-circle-plus-outline" />
              </el-button>
              <el-button
                type="text"
                size="mini"
                @click="() => remove(node, data)"
              >
                <i class="el-icon-delete" />
              </el-button>
            </span>
          </span>
        </el-tree>
      </div>
    </el-card>

    <div style="width: 79%; float: right">
      <el-table :data="caseData" border @row-click="caseRowClick">
        <el-table-column prop="id" label="ID" width="40"> </el-table-column>
        <el-table-column prop="name" label="名称" min-width="12%">
        </el-table-column>
        <el-table-column prop="module.name" label="所属模块" min-width="12%">
        </el-table-column>
        <el-table-column prop="method" label="请求类型" min-width="5%">
        </el-table-column>
        <el-table-column prop="url" label="URL" width="220"> </el-table-column>
        <el-table-column prop="create_time" label="创建时间" min-width="12%">
        </el-table-column>
        <el-table-column prop="update_time" label="更新时间" min-width="12%">
        </el-table-column>
      </el-table>
    </div>
    <!--      抽屉-->
    <el-drawer :title="caseTitle" :visible.sync="drawer" direction="rtl">
      <caseDialog v-if="drawer" :mid="currentModule" :cid="caseId" />
    </el-drawer>
    <caseModuleDialog
      v-if="dialogFlag"
      :rootId="rootFlag"
      :pid="projectValue"
      :proLabel="projectLabel"
      :parentObj="parentObj"
      @cancel="closeDiglog"
    />
  </div>
  <!--引入子组件-->
</template>

<script>
import ProjectApi from "../../request/project";
import ModuleApi from "../../request/module";
import caseModuleDialog from "./caseModuleDialog";
import caseDialog from "./caseDialog";

export default {
  data() {
    return {
      rootFlag: true,
      dialogFlag: false,
      moduleDate: [],
      projectOptions: [],
      projectValue: 1,
      projectLabel: "",
      parentObj: {},
      caseData: [],
      drawer: false,
      caseTitle: "",
      value: "",
      currentModule: 0,
      caseId: 0,
    };
  },
  components: {
    caseModuleDialog,
    caseDialog,
  },
  mounted() {
    this.initProjectlist();
    this.initModulelist(this.projectValue);
  },
  methods: {
    append(data) {
      this.parentObj = data;
      this.dialogFlag = true;
      this.rootFlag = false;
    },
    remove(node, data) {
      ModuleApi.deleteModules(data.id).then((resp) => {
        if (resp.success === true) {
          this.$message.success("删除成功！");
          this.initModulelist(this.projectValue);
        } else {
          this.$message.error(resp.error.msg);
        }
      });
    },
    //初始化项目列表
    async initProjectlist() {
      const resp = await ProjectApi.getProjects(this.req);
      if (resp.success === true) {
        this.projectValue = resp.items[0].id;
        this.projectLabel = resp.items[0].name;
        for (let i = 0; i < resp.items.length; i++) {
          this.projectOptions.push({
            value: resp.items[i].id,
            label: resp.items[i].name,
          });
        }
      }
    },
    //修改选中的项目
    changeProject(value) {
      this.projectLabel = this.projectOptions.find(
        (item) => item.value === value
      ).label;
      this.projectValue = value;
      this.getCaselist();
      this.initModulelist(value);
    },
    //查询模块列表
    async initModulelist(pid) {
      const req = { project_id: pid };
      const resp = await ModuleApi.getProModule(req);
      if (resp.success === true) {
        this.moduleDate = resp.items;
      }
    },
    //创建根节点模块
    createRootModule() {
      this.dialogFlag = true;
      this.rootFlag = true;
    },
    //创建模块关闭
    closeDiglog() {
      this.dialogFlag = false;
      this.parentObj = {};
      this.initModulelist(this.projectValue);
    },
    //点击模块节点
    nodeClick(data) {
      console.log(data);
      this.getCaselist(data.id);
      this.currentModule = data.id;
    },
    //初始化用例列表
    async getCaselist(mid) {
      const resp = await ModuleApi.getModuleCases(mid);
      if (resp.success === true) {
        this.caseData = resp.items;
        this.$message.success("查询成功");
      }
    },
    createCase() {
      this.drawer = true;
      this.caseTitle = "创建用例";
      this.caseId = 0;
    },
    //点击后-title变为查看用例-拉开抽屉
    caseRowClick(row) {
      this.drawer = true;
      console.log(row);
      this.caseId = row.id;
      this.caseTitle = "调试用例";
    },
    onJsonChange(value) {
      console.log("value", value);
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.custom-tree-node {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 14px;
  padding-right: 8px;
}

h3 {
  margin: 40px 0 0;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #42b983;
}
</style>
