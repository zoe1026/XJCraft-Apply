import { Message } from 'element-ui'

export function notifySuccess(msg, { timeout = 5000 } = {}) {
  Message({
    message: msg,
    type: 'success',
    duration: timeout
  })
}

export function notifyWarn(msg, { timeout = 5000 } = {}) {
  Message({
    message: msg,
    type: 'warning',
    duration: timeout
  })
}
