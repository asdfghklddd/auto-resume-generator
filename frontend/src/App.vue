<script setup lang="ts">
import { ref } from 'vue'

const rawInput = ref('')
const isLoading = ref(false)
const errorMessage = ref('')

// The parsed AI data model
const resumeData = ref<any>(null)

async function generateResume() {
  if (!rawInput.value.trim()) return
  
  isLoading.value = true
  errorMessage.value = ''
  
  try {
    const response = await fetch('/api/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: rawInput.value })
    })
    
    if (!response.ok) {
        const err = await response.json()
        throw new Error(err.detail || 'Failed to generate resume')
    }
    
    resumeData.value = await response.json()
    
  } catch (e: any) {
    errorMessage.value = e.message
  } finally {
    isLoading.value = false
  }
}

function printResume() {
  window.print();
}
</script>

<template>
  <div class="min-h-screen pt-12 pb-24 bg-gray-50/50 print:bg-white print:p-0">
    <!-- Header -->
    <header class="fixed top-0 inset-x-0 bg-white/70 backdrop-blur-xl shadow-sm z-50 print:hidden border-b border-gray-200/50">
      <div class="max-w-[1400px] mx-auto px-4 sm:px-6 lg:px-8 h-[60px] flex items-center justify-between">
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 rounded-xl bg-gradient-to-br from-indigo-500 to-violet-600 flex items-center justify-center text-white font-bold text-xl shadow-[0_2px_10px_-3px_rgba(99,102,241,0.6)] border border-white/20">A</div>
          <h1 class="text-xl font-[800] tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-gray-900 to-gray-600">
            Auto Resume
            <span class="text-xs font-bold ml-1.5 px-2 py-0.5 rounded-full bg-indigo-50 text-indigo-600 border border-indigo-100">Beta</span>
          </h1>
        </div>
        <div class="flex items-center gap-4">
          <button 
            @click="printResume"
            class="px-4 py-1.5 text-sm font-semibold rounded-lg bg-gray-900 text-white shadow-md hover:bg-gray-800 transition-all hover:shadow-lg active:scale-95 flex items-center gap-2"
          >
            Export to PDF
          </button>
        </div>
      </div>
    </header>

    <main class="max-w-[1400px] mx-auto px-4 sm:px-6 lg:px-8 mt-12 print:mt-0 print:m-0 print:p-0">
      <div class="grid lg:grid-cols-[400px_1fr] xl:grid-cols-[450px_1fr] gap-8 print:block">
        
        <!-- Editor Section -->
        <div class="print:hidden space-y-6 h-[calc(100vh-120px)] sticky top-[84px] flex flex-col">
          
          <div class="bg-white rounded-2xl shadow-sm border border-gray-200/70 p-6 flex-shrink-0 relative overflow-hidden group">
            <h2 class="text-lg font-bold text-gray-900 mb-2 flex items-center gap-2">
              <span class="text-indigo-600">✨</span> AI Magic Editor
            </h2>
            <p class="text-sm text-gray-500 mb-4">Paste your messy job history, linkedin dump, or raw notes. The AI will perfectly structure and polish it into the STAR format.</p>
            
            <textarea 
              v-model="rawInput"
              class="w-full h-32 p-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 outline-none text-sm resize-none transition-all"
              placeholder="e.g. Worked at Google from 2020-2022, built a backend system in Python that made things 20% faster..."
            ></textarea>
            
            <p v-if="errorMessage" class="text-red-500 text-xs mt-2 font-medium">{{ errorMessage }}</p>

            <button 
              @click="generateResume"
              :disabled="isLoading || !rawInput.trim()"
              class="w-full mt-4 py-2.5 rounded-xl bg-gradient-to-r from-indigo-600 to-violet-600 text-white font-semibold text-sm shadow-md hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed transition-all flex items-center justify-center gap-2"
            >
              <span v-if="isLoading" class="animate-spin text-white">◒</span>
              <span>{{ isLoading ? 'AI is processing...' : 'Generate Resume Draft' }}</span>
            </button>
          </div>

          <!-- Manual Editor Switch (Draft State) -->
          <div class="bg-white rounded-2xl shadow-sm border border-gray-200/70 overflow-hidden flex-1 flex flex-col">
            <div class="border-b border-gray-100 bg-gray-50/50 p-4">
              <h3 class="text-sm font-bold text-gray-700">Manual Adjustments (Live Data)</h3>
            </div>
            <div class="p-4 flex-1 overflow-y-auto">
              <div v-if="resumeData" class="space-y-4">
                 
                 <!-- Simple editor bindings -->
                 <div>
                    <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">Full Name</label>
                    <input v-model="resumeData.full_name" class="w-full p-2 text-sm border border-gray-200 rounded-lg">
                 </div>
                 <div>
                    <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">Title</label>
                    <input v-model="resumeData.professional_title" class="w-full p-2 text-sm border border-gray-200 rounded-lg">
                 </div>
                 <div>
                    <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">Summary</label>
                    <textarea v-model="resumeData.summary" rows="4" class="w-full p-2 text-sm border border-gray-200 rounded-lg"></textarea>
                 </div>

                 <!-- List editors can be added here for Experience/Education -> For MVP keeping it simple -->
                 <p class="text-xs text-indigo-500 mt-4">Edit experiences directly in the live preview (coming soon), or re-prompt AI for large changes.</p>
              </div>
              <p v-else class="text-xs text-gray-400 text-center mt-10">Generate draft to edit data here.</p>
            </div>
          </div>
        </div>

        <!-- Preview Section (A4 Paper) -->
        <div class="print:w-full flex justify-center pb-12 w-full overflow-x-auto min-h-screen pt-4">
          <div class="bg-white shadow-[0_20px_40px_-15px_rgba(0,0,0,0.1)] border border-gray-100 print:shadow-none print:border-none mx-auto w-[210mm] min-h-[297mm] print:w-[210mm] print:min-h-full shrink-0 relative overflow-hidden">
             
             <!-- Decorative Background Motif Placeholder -->
             <div class="absolute top-0 right-0 w-64 h-64 bg-gradient-to-bl from-indigo-50/10 to-transparent -z-10 rounded-bl-full print:block"></div>

             <div class="p-12 h-full flex flex-col text-gray-900" id="resume-document">
                
                <!-- If No Data -->
                <div v-if="!resumeData" class="flex-1 flex items-center justify-center">
                  <div class="text-center text-gray-400 text-sm mt-32 italic">
                    The AI-generated resume preview will render here natively in HTML.
                  </div>
                </div>

                <!-- If Data Exists -->
                <template v-else>
                    <!-- Header -->
                    <header class="border-b-2 border-gray-900 pb-4 mb-6 relative">
                      <h1 class="text-[32px] font-extrabold tracking-tight leading-none mb-1">{{ resumeData.full_name }}</h1>
                      <p class="text-indigo-700 font-bold uppercase tracking-widest text-[11px]">{{ resumeData.professional_title }}</p>
                      <div class="flex flex-wrap items-center gap-x-4 gap-y-1 mt-3 text-[11px] text-gray-600 font-medium">
                        <span v-if="resumeData.contact.location">{{ resumeData.contact.location }}</span>
                        <span v-if="resumeData.contact.email">· {{ resumeData.contact.email }}</span>
                        <span v-if="resumeData.contact.phone">· {{ resumeData.contact.phone }}</span>
                        <span v-if="resumeData.contact.github">· {{ resumeData.contact.github }}</span>
                        <span v-if="resumeData.contact.linkedin">· {{ resumeData.contact.linkedin }}</span>
                        <span v-if="resumeData.contact.portfolio">· {{ resumeData.contact.portfolio }}</span>
                      </div>
                    </header>

                    <!-- Summary -->
                    <section class="mb-5" v-if="resumeData.summary">
                        <p class="text-[12px] leading-relaxed text-gray-800">{{ resumeData.summary }}</p>
                    </section>

                    <!-- Experience -->
                    <section class="mb-5" v-if="resumeData.experience && resumeData.experience.length">
                       <h2 class="text-[13px] font-bold uppercase tracking-widest text-gray-900 border-b border-gray-300 pb-1 mb-3">Professional Experience</h2>
                       <div v-for="(exp, idx) in resumeData.experience" :key="idx" class="mb-4">
                           <div class="flex justify-between items-baseline mb-1">
                               <h3 class="text-[13px] font-bold text-gray-900">{{ exp.title }} <span class="text-gray-500 font-normal">| {{ exp.company }}</span></h3>
                               <span class="text-[11px] font-semibold text-gray-500 tracking-wide">{{ exp.date_range }}</span>
                           </div>
                           <ul class="list-disc pl-5 space-y-1">
                               <li v-for="(highlight, hIdx) in exp.highlights" :key="hIdx" class="text-[11px] leading-relaxed text-gray-700 pl-1">
                                   {{ highlight }}
                               </li>
                           </ul>
                       </div>
                    </section>

                    <!-- Projects -->
                    <section class="mb-5" v-if="resumeData.projects && resumeData.projects.length">
                       <h2 class="text-[13px] font-bold uppercase tracking-widest text-gray-900 border-b border-gray-300 pb-1 mb-3">Projects & Technical Feats</h2>
                       <div v-for="(proj, idx) in resumeData.projects" :key="idx" class="mb-3">
                           <div class="flex justify-between items-baseline mb-1">
                               <h3 class="text-[13px] font-bold text-gray-900">{{ proj.name }}</h3>
                               <p class="text-[10px] text-gray-500 italic">{{ proj.technologies.join(', ') }}</p>
                           </div>
                           <ul class="list-disc pl-5 space-y-1">
                               <li v-for="(desc, dIdx) in proj.description" :key="dIdx" class="text-[11px] leading-relaxed text-gray-700 pl-1">
                                   {{ desc }}
                               </li>
                           </ul>
                       </div>
                    </section>
                    
                    <div class="grid grid-cols-2 gap-6">
                        <!-- Education -->
                        <section class="mb-5" v-if="resumeData.education && resumeData.education.length">
                           <h2 class="text-[13px] font-bold uppercase tracking-widest text-gray-900 border-b border-gray-300 pb-1 mb-3">Education</h2>
                           <div v-for="(edu, idx) in resumeData.education" :key="idx" class="mb-2">
                               <div class="flex justify-between items-baseline">
                                   <h3 class="text-[12px] font-bold text-gray-900">{{ edu.institution }}</h3>
                               </div>
                               <p class="text-[11px] text-gray-700">{{ edu.degree }} <span v-if="edu.gpa" class="font-semibold ml-1">(GPA: {{ edu.gpa }})</span></p>
                               <span class="text-[10px] text-gray-500">{{ edu.date_range }}</span>
                           </div>
                        </section>

                        <!-- Skills -->
                        <section class="mb-5" v-if="resumeData.skills && resumeData.skills.length">
                           <h2 class="text-[13px] font-bold uppercase tracking-widest text-gray-900 border-b border-gray-300 pb-1 mb-3">Technical Skills</h2>
                           <div class="flex flex-wrap gap-1.5">
                               <span v-for="(skill, idx) in resumeData.skills" :key="idx" class="text-[10px] font-medium bg-gray-100/80 text-gray-800 px-2.5 py-1 rounded border border-gray-200 print:bg-transparent print:border-gray-300 print:px-1 print:py-0 print:-ml-1">
                                   {{ skill }}<span class="hidden print:inline">,</span>
                               </span>
                           </div>
                        </section>
                    </div>

                </template>
             </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>
