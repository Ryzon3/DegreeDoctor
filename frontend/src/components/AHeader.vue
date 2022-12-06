<script>
import { useStore } from "../stores/store";
import DarkModeToggle from "./DarkModeToggle.vue";
import ProgressBar from "./ProgressBar.vue";

export default {
    components: {
        DarkModeToggle,
        ProgressBar,
    },
    data() {
        const plans = ["CS Plan", "ITWS Plan", "HASS Plan"];
        return {
            plan: false,
            selectedPlan: "CS Plan",
            filteredPlans: plans,
            planOptions: plans,
        };
    },
    methods: {
        selectPlan(val) {
            this.selectedPlan = val;
        },
        filterPlan(val) {
            this.filteredPlans = this.planOptions.filter((x) =>
                x.toLowerCase().includes(val.toLowerCase())
            );
        },
    },
};
</script>

<template>
    <q-header elevated class="bg-secondary text-white" height-hint="98">
        <q-toolbar>
            <q-toolbar-title>
                <q-avatar>
                    <img src="../assets/Degree_Doctor_logo.png" />
                </q-avatar>
                Degree Doctor
            </q-toolbar-title>

            <DarkModeToggle />

            <div class="q-pa-md">
                <q-btn
                    no-caps
                    label="My Plans"
                    color="primary"
                    @click="plan = true"
                ></q-btn>
                <q-dialog v-model="plan">
                    <q-card style="min-width: 350px">
                        <q-card-section>
                            <div class="text-h6">Pick a plan</div>
                        </q-card-section>

                        <q-card-section class="q-pt-none">
                            <h6 class="q-ma-none">
                                Current Plan: {{ selectedPlan }}
                            </h6>
                            <div class="card-contain">
                                <q-select
                                v-model="selectedPlan"
                                filled
                                use-input
                                input-debounce="0"
                                label="Search"
                                :options="filteredPlans"
                                style="width: 200px"
                                behavior="menu"
                                @input-value="filterPlan"
                            >
                                <template #no-option>
                                    <q-item>
                                        <q-item-section class="text-grey">
                                            No results
                                        </q-item-section>
                                    </q-item>
                                </template>
                            </q-select>
                            <div>
                                <ProgressBar />
                            </div>
                            </div>
                        </q-card-section>
                        <q-card-actions class="text-primary">
                            <q-btn v-close-popup flat label="Cancel"></q-btn>
                            <q-btn
                                v-close-popup
                                flat
                                label="Add new plan"
                                to="/quiz"
                            ></q-btn>
                        </q-card-actions>
                    </q-card>
                </q-dialog>
            </div>
        </q-toolbar>
    </q-header>
</template>

<style scoped>
.card-contain {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    padding-right: 1em;
}
</style>