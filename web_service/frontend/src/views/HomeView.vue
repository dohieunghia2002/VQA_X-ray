<template>
  <v-container>
    <h1 class="heading">MEDICAL X-RAY IMAGE<br />QUESTION ANSWERING SYSTEM</h1>

    <v-row style="margin-top: 2rem;">
      <v-col cols="6">
        <v-btn variant="flat" color="blue-darken-4" @click="clickInput()">
          Upload an image
        </v-btn>

        <input type="file" id="upload" accept="image/png, image/jpeg, image/jpg" hidden @change="displayUploadImg()">

        <div class="img__wrapper">
          <img class="img" src="../assets/logo_ctu.png" alt="ảnh upload">
        </div>
      </v-col>

      <v-col cols="6" class="result-detect__wrapper">
        <h3>Ask your question:</h3>

        <input type="text" id="question" class="input--question">

        <div class="answer__result">
          <v-btn variant="flat" color="green-darken-4" @click="predict()">
            Answer
          </v-btn>
          <p class="answer__content">{{ answer }}</p>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      answer: ''
    }
  },

  methods: {
    async displayUploadImg() {
      const inputElement = document.getElementById("upload");
      const file = inputElement.files[0];
      const imgElement = document.getElementsByClassName("img")[0];
      imgElement.src = URL.createObjectURL(file)
    },

    async clickInput() {
      const inputElement = document.getElementById("upload");
      inputElement.click();
    },

    async predict() {
      const inputImgElement = document.getElementById("upload");
      const file = await inputImgElement.files[0];
      const inputTxtElement = document.getElementById("question");
      const contentQuestion = await inputTxtElement.value;

      const form = new FormData()
      form.append('file', file)
      form.append('question', contentQuestion)

      const res = await axios.post('http://127.0.0.1:9999/api/predict', form, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      this.answer = res.data.answer;
    }
  }
}
</script>

<style scoped>
.heading {
  text-align: center;
}

.img__wrapper {
  margin-top: 2rem;
  width: 60%;
}

img {
  width: 100%;
}

.input--question {
  border: 2px solid #222;
  width: 80%;
  font-size: 1.4em;
  margin-top: .5rem;
}

.answer__result {
  margin-top: 1.5rem;
}

.answer__content {
  font-size: 3em;
}
</style>