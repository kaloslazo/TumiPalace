<template>
	<section id="heroWrapper" class="px-6 mt-5 mx-auto justify-center items-center flex flex-col lg:flex-row">

    <div id="leftAction" class="lg:mr-5 my-5 text-center mb-16 lg:text-left">
        <h3 class="text-white font-bold text-center lg:text-left text-5xl lg:mr-14 max-w-xl lg:max-w-xs lg:text-5xl">Crea tu cuenta y recibe un bono de bienvenida de hasta</h3>
        <h5 class="my-8 font-bold text-yellow-600 text-5xl mb-12">S/. 1,000</h5>
        <router-link class="bg-yellow-600 px-10 py-2 rounded-sm font-medium border-2 border-yellow-600 hover:bg-yellow-700 text-base hover:border-yellow-700 transition-all" to="/register">Reclamar bono</router-link>
    </div>

    <div id="rightAction" class="flex flex-row gap-5">
        <div class="bg-brown-1000 py-5 px-5 mx-auto max-w-xs">
            <img src="../assets/img/rouletteGame/cardRoulette.png" alt="cardRoulette" class="w-40 mx-auto mb-6">
            <a class="text-yellow-600 font-semibold text-lg border-b-2 block mb-4 pb-2" href="{{url_for('register')}}">Ruleta del Inca</a>
            <p class="text-grey-300 text-sm">Recibe el botín Inca apostando por tus números de la suerte.</p>
        </div>
        <div class="bg-brown-1000 py-5 px-5 mx-auto max-w-xs">
            <img src="../assets/img/slotsGame/cardSlots.png" alt="cardSlots" class="w-40 mx-auto mb-3">
            <a class="text-yellow-600 font-semibold text-lg border-b-2 block mb-4 pb-2" href="{{url_for('register')}}">Fortuna del Sol</a>
            <p class="text-grey-300 text-sm">Obtén 3 figuras idénticas y prepárate para ganar hasta S/.100,000!</p>
        </div>
    </div>

  </section>
</template>
  
<script>
</script>