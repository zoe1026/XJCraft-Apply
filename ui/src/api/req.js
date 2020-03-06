import request from '@/utils/request'

export function req(data) {
  return request({
    url: '/player/req',
    method: 'post',
    data
  })
}
