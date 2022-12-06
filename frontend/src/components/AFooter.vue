<script>
export default {
    name: "AFooter",
};
</script>

<template>
    <q-footer elevated class="bg-grey-8 text-white">
        <q-toolbar>
            <q-toolbar-title id="footer" class="text-center q-py-xs">
                <div id="text" class="text-subtitle2">We love your feedback!</div>
                <a href="https://github.com/Ryzon3/DegreeDoctor">
                    <q-icon id="icon" name="fa-brands fa-github" size="35px" />
                </a>
                <p id="copy">&copy; 2022 Degree Doctor</p>
            </q-toolbar-title>
        </q-toolbar>
    </q-footer>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif:ital,wght@0,400;0,700;1,400;1,700&display=swap');

#footer {
    font-size: 0.9em;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
}

a {
    color: white;
    text-decoration: none;
}

#icon {
    transition: 0.5s;
}

#icon:hover {
    transform: scale(1.2);
}

#copy {
    font-size: 1.1em;
    color: white;
    padding-top: 15px;
}

#text {
    font-size: 1.1rem;
    font-family: 'Noto Serif', serif;
}

</style>
