<template>
  <div style="margin-left: 10px; margin-right: 10px" class="div-line">
    <div style="height: 50px">
      <el-select
        v-model="caseForm.method"
        placeholder="方法"
        size="small"
        style="width: 15%; float: left"
      >
        <el-option
          v-for="item in methodOptions"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        />
      </el-select>
      <el-input
        v-model="caseForm.url"
        placeholder="URL"
        size="small"
        style="float: left; width: 70%"
        >URL</el-input
      >
      <el-button
        type="primary"
        plain
        style="float: left; width: 10%"
        size="small"
        @click="sendCase"
        >发送</el-button
      >
    </div>
    <div>
      <el-radio v-model="caseForm.params_type" label="params">params</el-radio>
      <el-radio v-model="caseForm.params_type" label="form">Form-date</el-radio>
      <el-radio v-model="caseForm.params_type" label="json">JSON</el-radio>
    </div>
    <div style="height: 220px">
      <el-tabs v-model="activeName">
        <el-tab-pane label="Headers" name="first">
          <vueJsonEditor v-model="caseForm.header" :mode="'code'" />
        </el-tab-pane>
        <el-tab-pane label="Params/Body" name="second">
          <vueJsonEditor v-model="caseForm.params_body" :mode="'code'" />
        </el-tab-pane>
      </el-tabs>
    </div>
    <div style="height: 200px">
      <i style="float: left">response:</i>
      <el-input
        v-model="caseForm.response"
        type="textarea"
        :rows="7"
        placeholder="Response"
      />
    </div>
    <div>
      <el-collapse v-model="activeNames">
        <el-collapse-item title="断 言" name="2">
          <div style="height: 30px">
            <el-radio v-model="caseForm.assert_type" label="include"
              >include</el-radio
            >
            <el-radio v-model="caseForm.assert_type" label="equal"
              >equal</el-radio
            >
            <el-button
              class="debug-button"
              type="success "
              plain
              size="small"
              @click="assertClick"
              >断 言</el-button
            >
          </div>
          <div>
            <el-input
              v-model="caseForm.assert_text"
              type="textarea"
              :rows="5"
              placeholder="assertequal"
            />
          </div>
        </el-collapse-item>
      </el-collapse>
    </div>
    <div style="height: 70px">
      <el-input
        v-model="caseForm.name"
        placeholder="用例名称"
        size="small"
        style="float: left; width: 80%"
        >case</el-input
      >
      <el-button
        type="primary"
        plain
        style="float: left; width: 10%"
        size="small"
        @click="saveClick()"
        >保 存</el-button
      >
    </div>
  </div>
</template>

<script>
import vueJsonEditor from "vue-json-editor";
import CasesApi from "../../request/cases";
export default {
  props: ["mid", "cid"],
  name: "caseDialog",
  components: {
    vueJsonEditor,
  },
  data() {
    return {
      methodOptions: [
        { value: "get", label: "GET" },
        { value: "post", label: "POST" },
        { value: "put", label: "PUT" },
        { value: "delete", label: "DELETE" },
      ],
      value: "",
      activeNames: ["1"],
      activeName: "second",
      caseForm: {
        name: "",
        module_id: 0,
        url: "",
        method: "get",
        header: {},
        params_type: "params",
        params_body: {},
        response: "",
        assert_type: "include",
        assert_text: "",
      },
    };
  },
  mounted() {
    this.caseForm.module_id = this.mid;
    if (this.cid !== 0) {
      this.getInfoCase();
    }
  },
  methods: {
    //查询单个用例详情
    async getInfoCase() {
      const resp = await CasesApi.getCases(this.cid);
      if (resp.success === true) {
        this.caseForm = resp.item;
        console.log(resp.item);
        const header = resp.item.header.replace(/'/g, '"');
        const params_body = resp.item.params_body.replace(/'/g, '"');
        this.caseForm.header = JSON.parse(header);
        this.caseForm.params_body = JSON.parse(params_body);
      } else {
        this.$message.error(resp.error.msg);
      }
    },

    //请求；调试接口
    async sendCase() {
      const req = {
        method: this.caseForm.method,
        url: this.caseForm.url,
        header: JSON.stringify(this.caseForm.header),
        params_type: this.caseForm.params_type,
        params_body: JSON.stringify(this.caseForm.params_body),
      };
      const resp = await CasesApi.casesDebug(req);
      if (resp.success === true) {
        this.caseForm.response = resp.item.response;
        console.log("resp:", resp);
      } else {
        console.log("res___", resp);
      }
    },
    //断言用例
    async assertClick() {
      const req = {
        response: this.caseForm.response,
        assert_type: this.caseForm.assert_type,
        assert_text: this.caseForm.assert_text,
      };
      const resp = await CasesApi.assertCase(req);
      if (resp.success === true) {
        console.log("resp:", resp);
        this.$message.success("断言成功");
      } else {
        console.log("res___", resp);
        this.$message.error("断言失败");
      }
    },
    //保存用例
    async saveClick() {
      if (this.cid === 0) {
        const resp = await CasesApi.createCase(this.caseForm);
        if (resp.success === true) {
          this.$message.success("保存成功");
        } else {
          this.$message.error(resp.error.msg);
        }
      } else {
        const resp = await CasesApi.updateCases(this.cid, this.caseForm);
        if (resp.success === true) {
          this.$message.success("编辑成功");
        } else {
          this.$message.error(resp.error.msg);
        }
      }
    },
  },
};
</script>

<style>
div.jsoneditor {
  border: thin solid #ced4da;
}

div.jsoneditor-menu {
  display: none;
}

.ace-jsoneditor .ace_gutter {
  background: white;
}

div.jsoneditor-outer.has-main-menu-bar {
  margin-top: 0;
  padding-top: 0;
}

.per-label {
  margin-right: 10px;
  margin-bottom: 4px;
  font-size: 1rem;
}
</style>

<style scoped>
.debug-button {
  float: right;
  margin-right: 50px;
}

.div-line {
  height: auto;
  width: 100%;
  text-align: left;
  margin-bottom: 10px;
}
</style>
