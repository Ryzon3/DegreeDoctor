<script>
import { useStore } from "../stores/store";

export default {
    name: 'ProgressBar',
    data() {
        return {
            store: useStore(),
        }
    },
    computed: {
        percent() {
            let total = 0;
            let courses = this.store.getCredits;
            for (const name in courses) {
                total += courses[name];
            }
            return Math.round(total / 128 * 100);
        }
    }
}
</script>

<template>
    <q-circular-progress
        show-value
        font-size="12px"
        :value="percent"
        size="50px"
        :thickness="0.22"
        color="teal"
        track-color="grey-3"
        class="q-ma-md"
    >
    {{ percent }}%
    </q-circular-progress>

</template>