<template lang="pug">
    div(style="padding-top: 10px; line-height: 30px;")
      el-badge(:value="taskGroups.length > 0 ? '+' : ''", :type="currentTask ? 'danger' : 'success'")
        svg-icon.list-icon(icon-class="list", @click="showFlag = true")

      el-dialog(:visible.sync="showFlag", title="任务列表", width="90%")
        el-card.box-card(v-for="(taskGroup, idx) in taskGroups", :key="idx")
          .clearfix(slot="header")
            span {{ taskGroup.name }}
            el-button(v-if="taskGroup.finishCount !== taskGroup.totalCount", type="warning", style="float: right", @click="cancelAll(taskGroup)") 全部取消
            el-button(v-else, icon="el-icon-close", type="primary", style="float: right", @click="removeGroup(taskGroup)")
          el-row
            el-progress(:percentage="Math.round(taskGroup.finishCount / taskGroup.totalCount * 100)")
          el-row
            el-table(
              :data="taskGroup.tasks",
              border,
              fit,
              highlight-current-row,
              style="margin-top: 20px;"
            )
              el-table-column(label="#", type="index", align="center")
              el-table-column(label="任务", prop="name", align="center")
              el-table-column(label="状态", width="120px", align="center")
                template(slot-scope="{row}")
                  el-tooltip(:content="row.control.msg", effect="dark", placement="bottom", :disabled="!row.control.msg")
                    el-tag(:type.sync="statusType[row.control.status]")
                      | {{ row.control.status | statusFilter }}
                      i.el-icon-loading(v-if="row.control.status === 1")
              el-table-column(label="操作", width="100px", align="center")
                template(slot-scope="{row}")
                  el-button(v-if="row.control.status === 0", type="warning", icon="el-icon-error", @click="row.control.cancel()")
</template>

<script>
import Vue from 'vue'

const statusNames = ['等待中...', '进行中...', '已完成', '已取消', '失败']

export default {
  name: 'TaskList',
  filters: {
    statusFilter(type) {
      return statusNames[type]
    }
  },
  data() {
    return {
      showFlag: false,
      statusType: [
        'info',
        'medium',
        'success',
        'warning',
        'danger'
      ],

      currentTask: (void 0),
      taskGroups: []
    }
  },
  methods: {
    submitTask(tasks, name) {
      const group = {
        name,
        totalCount: tasks.length,
        finishCount: 0,
        tasks,
        self: this,

        start() {
          Vue.nextTick(() => this.tasks[0].control.start())
        }
      }

      var prev
      tasks.forEach(task => {
        task.control = {
          status: 0,
          task,
          group,
          msg: '',
          self: this,

          finish(msg = '') {
            this.msg = msg
            this.status = 2
            group.finishCount += 1
            this.toNext()
          },
          fail(msg = '') {
            this.msg = msg
            this.status = 4
            group.finishCount += 1
            this.toNext()
          },

          cancel() {
            this.status = 3
            group.finishCount += 1
          },
          start() {
            if (this.status === 0) {
              this.currentTask = this.task
              this.status = 1
              this.task.task(this)
            } else {
              this.toNext()
            }
          },
          toNext() {
            if (this.next) {
              Vue.nextTick(() => this.next.start())
            } else {
              this.self.toNextGroup(group)
            }
          }
        }

        if (prev) prev.next = task.control
        prev = task.control
      })

      if (this.taskGroups.length > 0) {
        this.taskGroups[this.taskGroups.length - 1].next = group
        group.prev = this.taskGroups[this.taskGroups.length - 1]
      }
      this.taskGroups.push(group)

      if (this.currentTask === (void 0)) {
        this.currentTask = tasks[0]
        group.start()
      }
    },
    toNextGroup(currentGroup) {
      if (currentGroup.next) {
        currentGroup.next.start()
      } else {
        this.currentTask = (void 0)
      }
    },
    cancelAll(group) {
      group.tasks
        .filter(e => e.control.status === 0)
        .forEach(e => e.control.cancel())
    },
    removeGroup(group) {
      const index = this.taskGroups.indexOf(group)
      this.taskGroups.splice(index, 1)

      if (group.prev) group.prev.next = (void 0)
      if (group.next) group.next.prev = (void 0)
      if (group.prev && group.next) group.prev.next = group.next
    },
    show() {
      this.showFlag = true
    }
  }

}
</script>
