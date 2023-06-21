<template>
    <div>
        <h1>Create Department:</h1>
        <form @submit.prevent="createDepartmentEvent">
            <div class="form-group">
                <label>Name:</label>
                <input type="text" v-model.trim="department.name" />
            </div>
            <div class="form-group">
                <label>Short Name:</label>
                <input type="text" v-model.trim="department.short_name" />
            </div>
            <button type="submit" class="submit-button">Submit</button>
        </form>
    </div>
</template>

<script>
import { createDepartment } from '@/services/departmentService.api.js';
export default {
    name: "DepartmentCreation",
    data() {
        return {
            department: {
                name: '',
                short_name: '',
            },
        };
    },
    methods: {
        async createDepartmentEvent() {
            const response = await createDepartment(this.department);
            console.log("response = ", response);
        },
    },
};
</script>

<style>
.form-group {
    margin-bottom: 1rem;
}

input[type="text"] {
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
    width: 300px;
}

label {
    display: block;
    margin-bottom: 5px;
}

.submit-button {
    background-color: green;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}
</style>