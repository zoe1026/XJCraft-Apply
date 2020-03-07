import Layout from '@/layout'

const playerRouter = {
  path: '/player',
  component: Layout,
  redirect: 'noRedirect',
  name: 'Player',
  meta: {
    title: '玩家',
    icon: 'peoples',
    roles: ['OP']
  },
  children: [
    {
      path: 'req-list',
      component: () => import('@/views/player/req-list'),
      name: '玩家申请列表',
      meta: {
        title: '玩家申请列表'
      }
    },
    {
      path: 'ip-black-list',
      component: () => import('@/views/player/ip-black-list'),
      name: 'IP 黑名单',
      meta: {
        title: 'IP 黑名单'
      }
    }
  ]
}
export default playerRouter
