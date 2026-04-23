import request from './request'

export const login = (data) => request.post('/admin/login', data)
export const verifyToken = (token)  => request.post('/admin/verify', { params: {token} })