import { createStore } from 'vuex'
import axios from 'axios'

export default createStore({
    state: {
        status: '',
        user: {},
        user_data: {},
        token: localStorage.getItem('user') ? JSON.parse(localStorage.getItem('user')).token : ''
    },
    mutations: {
        auth_request(state) {
            state.status = 'loading'
        },
        auth_success(state, user) {
            state.status = 'success'
            state.user = user
        },
        auth_error(state, err) {
            state.status = 'error'
        },
        logout(state) {
            state.status = ''
            state.user = {}
        },
        updateUser(state, updatedUser) {
            // usar destructuring: actualizar lo necesario
            state.user_data = { ...state.user_data, ...updatedUser };
        },
    },
    actions: {
        async login({ commit }, user) {
            commit('auth_request')
            try {
                const res = await axios.post('login', user);

                this.state.user_data = res.data.user;
                if (res.data.access_token) {
                    const user = { token: res.data.access_token };
                    localStorage.setItem('user', JSON.stringify(user));
                    axios.defaults.headers.common['Authorization'] = "Bearer " + user.token;
                    commit('auth_success', user);
                }
                return res
            } catch (err) {
                commit('auth_error');
                localStorage.removeItem('user');
                throw err;
            }
        },
        async logout({ commit }) {
            commit('logout')
            localStorage.removeItem('user')
            delete axios.defaults.headers.common['Authorization']
        }
    },
    getters: {
        isLoggedIn: state => !!state.user.token,
        authStatus: state => state.status,
        user: state => state.user,
        user_data: state => state.user_data,
    },
})