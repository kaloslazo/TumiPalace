import axios from "axios";

export default {
    async registerUser(username, password, email, age){
        try {
            const response = await axios.post("register", { username, password, email, age });
            return response.data;
        } catch(err) {
            console.log(err);
            throw err; 
        }
    }
};