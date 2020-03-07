<template lang="pug">
  .app-container
    .filter-container
      el-button.filter-item(v-waves, type="primary", icon="el-icon-search", @click="getList")

    el-table(
      v-loading="listLoading",
      :data="list",
      border,
      fit,
      highlight-current-row,
      style="width: 100%;",
      @cell-dblclick="row => row.edit = true"
    )
      el-table-column(label="玩家名", prop="playerName", align="center")
      el-table-column(label="密码", prop="password", align="center")
      el-table-column(label="申请时间", align="center")
        template(slot-scope="{row}")
          span {{ row.reqTime | timestampFilter }}
      el-table-column(label="审核时间", align="center")
        template(slot-scope="{row}")
          span {{ row.applyTime | timestampFilter }}
      el-table-column(label="审核人", prop="applyOP", align="center")
      el-table-column(label="状态", align="center")
        template(slot-scope="{row}")
          span {{ row.status | statusFilter }}
      el-table-column(label="申请类型", align="center")
        template(slot-scope="{row}")
          span {{ row.type | typeFilter }}
      el-table-column(label="IP", prop="ip", align="center")
      el-table-column(label="QQ", prop="qq", align="center")
      el-table-column(align="center")
        template(slot="header")
          el-tooltip(content="对于老玩家邀请，此处为邀请人，对于 OP 线下沟通，此处为 OP 名", effect="dark", placement="bottom")
            label 关系人&nbsp;
              i.el-icon-info
        template(slot-scope="{row}")
          span {{ row.type === 'Invite' ? row.oldPlayerName : row.opName }}
      el-table-column(label="审批", align="center", width="160px")
        template(slot-scope="{row}")
          el-button(v-if="row.status === 'NEW'", size="mini", type="success", icon="el-icon-check", @click="handleApply(row, 'ACCEPT')")
          el-button(v-if="row.status === 'NEW'", size="mini", type="warning", icon="el-icon-close", @click="handleApply(row, 'DENY')")

    pagination(v-show="total>0", :total="total", :page.sync="listQuery.page", :limit.sync="listQuery.pageSize", @pagination="getList")
</template>

<script>
import { fetchReqList, apply } from '@/api/req'
import { notifySuccess } from '@/utils/notify'
import Pagination from '@/components/Pagination'

const types = {
  QQLevel: 'QQ 等级过太阳',
  Invite: '老玩家邀请',
  PYJY: 'OP 线下沟通'
}
const statuses = {
  NEW: '待处理',
  ACCEPT: '已通过',
  DENY: '已拒绝'
}

export default {
  name: 'ReqList',
  components: { Pagination },
  filters: {
    typeFilter(val) {
      return types[val]
    },
    statusFilter(val) {
      return statuses[val]
    }
  },
  data() {
    return {
      listQuery: {
        page: 1,
        pageSize: 20
      },
      list: [],
      total: 0,
      listLoading: true,
      types,
      statuses
    }
  },
  mounted() {
    this.getList()
  },
  methods: {
    getList() {
      this.listLoading = true
      fetchReqList(this.listQuery).then(response => {
        this.list = response.data.list
        this.total = response.data.totalRow
        this.listQuery.page = response.data.page

        // 取消加载动画
        setTimeout(() => {
          this.listLoading = false
        }, 100)
      })
    },
    handleApply(row, result) {
      apply({
        playerName: row.playerName,
        result
      }).then(response => {
        notifySuccess(result === 'ACCEPT' ? '审核成功' : '拒绝成功')

        row.status = result
      })
    }
  }
}
</script>

<style scoped>
</style>
