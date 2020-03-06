import { Message } from 'element-ui'

export function notifySuccess(msg, { timeout = 4000 } = {}) {
  Message({
    message: msg,
    type: 'success',
    duration: timeout
  })
}

export function notifyWarn(msg, { timeout = 4000 } = {}) {
  Message({
    message: msg,
    type: 'warning',
    duration: timeout
  })
}
