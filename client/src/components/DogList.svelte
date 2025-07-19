<script lang="ts">
    import { onMount } from "svelte";

    interface Dog {
        id: number;
        name: string;
        breed: string;
        status?: string;
    }
    interface Breed {
        id: number;
        name: string;
    }

    export let dogs: Dog[] = [];
    let breeds: Breed[] = [];
    let selectedBreed: number | null = null;
    let onlyAvailable: boolean = false;
    let loading = true;
    let error: string | null = null;
    let theme: 'dark' | 'light' = 'dark';

    const fetchBreeds = async () => {
        try {
            const response = await fetch('/api/breeds');
            if (response.ok) {
                breeds = await response.json();
            }
        } catch {}
    };

    const fetchDogs = async () => {
        loading = true;
        let url = '/api/dogs';
        try {
            const response = await fetch(url);
            if(response.ok) {
                let allDogs: Dog[] = await response.json();
                let filtered = allDogs;
                if (selectedBreed !== null) {
                    filtered = filtered.filter(d => breeds.find(b => b.id === selectedBreed)?.name === d.breed);
                }
                if (onlyAvailable) {
                    filtered = filtered.filter(d => d.status === 'Available');
                }
                dogs = filtered;
            } else {
                error = `Failed to fetch data: ${response.status} ${response.statusText}`;
            }
        } catch (err) {
            error = `Error: ${err instanceof Error ? err.message : String(err)}`;
        } finally {
            loading = false;
        }
    };

    const refresh = () => {
        fetchDogs();
    };

    const toggleTheme = () => {
        theme = theme === 'dark' ? 'light' : 'dark';
        document.documentElement.classList.toggle('dark', theme === 'dark');
        document.documentElement.classList.toggle('light', theme === 'light');
    };

    onMount(() => {
        fetchBreeds();
        fetchDogs();
        document.documentElement.classList.add('dark');
    });

    $: selectedBreed, refresh();
    $: onlyAvailable, refresh();
</script>

<div class={`min-h-screen py-8 px-4 transition-colors duration-500 ${theme === 'dark' ? 'bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-slate-100' : 'bg-gradient-to-br from-white via-slate-100 to-white text-slate-900'}`}>
    <div class="flex flex-col md:flex-row md:items-center md:justify-between mb-8 gap-4">
        <h2 class="text-3xl font-bold mb-2 md:mb-0 tracking-tight">Available Dogs</h2>
        <div class="flex gap-4 items-center">
            <select class="bg-slate-800 text-slate-100 dark:bg-slate-800 dark:text-slate-100 light:bg-white light:text-slate-900 border border-slate-700 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all" bind:value={selectedBreed}>
                <option value={null}>All Breeds</option>
                {#each breeds as breed}
                    <option value={breed.id}>{breed.name}</option>
                {/each}
            </select>
            <label class="flex items-center gap-2 cursor-pointer">
                <input type="checkbox" bind:checked={onlyAvailable} class="accent-blue-500" />
                <span class="text-base">Available only</span>
            </label>
            <button class="ml-2 px-4 py-2 rounded-lg font-medium shadow bg-blue-600 text-white hover:bg-blue-700 transition-colors duration-300" on:click={toggleTheme} aria-label="Toggle theme">
                {theme === 'dark' ? 'Light Mode' : 'Dark Mode'}
            </button>
        </div>
    </div>

    {#if loading}
        <!-- loading animation -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {#each Array(6) as _, i}
                <div class="bg-slate-800/60 backdrop-blur-sm rounded-xl overflow-hidden shadow-lg border border-slate-700/50">
                    <div class="p-6">
                        <div class="animate-pulse">
                            <div class="h-6 bg-slate-700 rounded w-3/4 mb-3"></div>
                            <div class="h-4 bg-slate-700 rounded w-1/2 mb-4"></div>
                            <div class="h-4 bg-slate-700 rounded w-1/4 mt-6"></div>
                        </div>
                    </div>
                </div>
            {/each}
        </div>
    {:else if error}
        <!-- error display -->
        <div class="text-center py-12 bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700">
            <p class="text-red-400">{error}</p>
        </div>
    {:else if dogs.length === 0}
        <!-- no dogs found -->
        <div class="text-center py-12 bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700">
            <p class="text-slate-300">No dogs available at the moment.</p>
        </div>
    {:else}
        <!-- dog list -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {#each dogs as dog (dog.id)}
                <a 
                    href={`/dog/${dog.id}`} 
                    class="group block bg-slate-800/60 backdrop-blur-sm rounded-xl overflow-hidden shadow-lg border border-slate-700/50 hover:border-blue-500/50 hover:shadow-blue-500/10 hover:shadow-xl transition-all duration-300 hover:translate-y-[-6px]"
                >
                    <div class="p-6 relative">
                        <div class="absolute inset-0 bg-gradient-to-r from-blue-600/10 to-purple-600/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                        <div class="relative z-10">
                            <h3 class="text-xl font-semibold mb-2 group-hover:text-blue-400 transition-colors">{dog.name}</h3>
                            <p class="text-slate-400 mb-2">{dog.breed}</p>
                            {#if dog.status}
                                <span class="inline-block px-2 py-1 rounded text-xs font-semibold mb-2 {dog.status === 'Available' ? 'bg-green-600 text-white' : 'bg-slate-700 text-slate-300'}">{dog.status}</span>
                            {/if}
                            <div class="mt-4 text-sm text-blue-400 font-medium flex items-center">
                                <span>View details</span>
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 ml-1 transform transition-transform duration-300 group-hover:translate-x-2" viewBox="0 0 20 20" fill="currentColor">
                                    <path fill-rule="evenodd" d="M12.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-2.293-2.293a1 1 0 010-1.414z" clip-rule="evenodd" />
                                </svg>
                            </div>
                        </div>
                    </div>
                </a>
            {/each}
        </div>
    {/if}
</div>