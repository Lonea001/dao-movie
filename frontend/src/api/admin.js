import request from './request'

export const login = (data) => request.post('/admin/login', data)
export const verifyToken = (token)  => request.get('/admin/verify', { params: {token} })