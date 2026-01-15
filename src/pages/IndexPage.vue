<template>
  <q-page
    :class="[$q.dark.isActive ? 'bg-grey-9' : 'bg-grey-2']"
    class="q-pa-md flex flex-center column"
    style="min-height: 100vh"
  >
    <q-card class="q-pa-lg shadow-10" style="max-width: 500px; width: 100%">
      <q-card-section align="center">
        <q-avatar size="100px" class="bg-primary">
          <q-img src="../assets/logo.png" alt="Logo" />
        </q-avatar>
      </q-card-section>

      <q-card-section>
        <div class="text-h5 text-primary">🔐 {{ t('title') }}</div>
        <div class="text-caption text-grey">{{ t('description') }}</div>
      </q-card-section>

      <q-card-section>
        <q-input
          filled
          v-model="password"
          :type="showPassword ? 'text' : 'password'"
          :label="t('enterPassword')"
        >
          <template #append>
            <q-icon
              :name="showPassword ? 'visibility_off' : 'visibility'"
              class="cursor-pointer"
              @click="showPassword = !showPassword"
              :aria-label="showPassword ? t('hidePassword') : t('showPassword')"
            />
          </template>
        </q-input>

        <div v-if="password.length >= 1" class="q-mt-md">
          <q-linear-progress
            :value="score / 4"
            :color="progressColor"
            size="15px"
            rounded
            :aria-label="t('passwordStrengthIndicator')"
          />
          <div class="q-mt-sm text-subtitle2">{{ t('strength') }} : {{ strengthLabel }}</div>

          <ul v-if="feedback.suggestions.length" class="q-mt-sm text-caption">
            <li v-for="(s, index) in translatedSuggestions" :key="index">{{ s }}</li>
          </ul>

          <div v-if="isCheckingPwned" class="text-primary q-mt-sm">
            {{ t('checkingLeaks') }}
          </div>
          <div v-else-if="pwnedCount > 0" class="text-negative q-mt-sm">
            {{ t('foundInLeaks', { count: pwnedCount }) }} ⚠️
          </div>
          <div v-else-if="pwnedChecked" class="text-positive q-mt-sm">
            {{ t('notFoundInLeaks') }} ✅
          </div>
        </div>
      </q-card-section>

      <q-separator class="q-my-md" />

      <q-card-section>
        <div class="text-h6">🔧 {{ t('passwordGenerator') }}</div>
        <q-slider
          v-model="genLength"
          :min="6"
          :max="32"
          label
          label-always
          :aria-label="t('passwordLength')"
        />

        <div class="q-gutter-sm q-my-sm">
          <q-toggle v-model="useUppercase" :label="t('uppercase')" />
          <q-toggle v-model="useNumbers" :label="t('numbers')" />
          <q-toggle v-model="useSymbols" :label="t('symbols')" />
        </div>

        <q-input filled readonly v-model="generatedPassword" :label="t('generatedPassword')" />
        <div class="q-gutter-sm q-mt-sm">
          <q-btn icon="refresh" :label="t('generate')" @click="generatePassword" color="primary" />
          <q-btn
            icon="content_copy"
            :label="t('copy')"
            @click="copyToClipboard(generatedPassword)"
            color="secondary"
          />
        </div>
      </q-card-section>

      <q-card-actions align="between" class="q-mt-md">
        <q-toggle v-model="darkMode" :label="t('darkMode')" color="grey-8" />
        <q-btn flat dense icon="translate" @click="toggleLang" :label="currentLang.toUpperCase()" />
      </q-card-actions>
    </q-card>
  </q-page>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue';
import zxcvbn from 'zxcvbn';
import type { ZXCVBNFeedback } from 'zxcvbn';
import sha1 from 'crypto-js/sha1';
import encHex from 'crypto-js/enc-hex';
import { useQuasar } from 'quasar';

const $q = useQuasar();
const password = ref('');
const showPassword = ref(false);
const score = ref(0);
const feedback = ref<ZXCVBNFeedback>({ warning: '', suggestions: [] });
const pwnedCount = ref(0);
const isCheckingPwned = ref(false);
const pwnedChecked = ref(false);

const darkMode = ref(false);
onMounted(() => {
  $q.dark.set(window.matchMedia('(prefers-color-scheme: dark)').matches);
  darkMode.value = $q.dark.isActive;
});
watch(darkMode, (val) => $q.dark.set(val));

const checkPassword = async () => {
  const result = zxcvbn(password.value);
  score.value = result.score;
  feedback.value = result.feedback;
  await checkPwned(password.value);
};

const checkPwned = async (pwd: string) => {
  if (!pwd) return;
  isCheckingPwned.value = true;
  pwnedChecked.value = false;

  const hash = sha1(pwd).toString(encHex).toUpperCase();
  const prefix = hash.slice(0, 5);
  const suffix = hash.slice(5);

  try {
    const response = await fetch(`https://api.pwnedpasswords.com/range/${prefix}`);
    const text = await response.text();
    const lines = text.split('\n');
    const match = lines.find((line) => line.startsWith(suffix));

    if (match) {
      const count = match ? parseInt(match.split(':')[1] || '0') : 0;
      pwnedCount.value = count;
    } else {
      pwnedCount.value = 0;
    }
  } catch (err) {
    console.error('Erreur lors de la vérification Pwned:', err);
  } finally {
    isCheckingPwned.value = false;
    pwnedChecked.value = true;
  }
};

watch(password, (val) => {
  if (val.length >= 1) void checkPassword();
});

const strengthLabel = computed(() => {
  const labels =
    currentLang.value === 'fr'
      ? ['Très faible', 'Faible', 'Moyenne', 'Bonne', 'Excellente']
      : ['Very weak', 'Weak', 'Medium', 'Strong', 'Excellent'];
  return labels[score.value] || 'Unknown';
});

const progressColor = computed(() => {
  const colors = ['negative', 'warning', 'warning', 'positive', 'positive'];
  return colors[score.value];
});

// Password Generator
const genLength = ref(16);
const useUppercase = ref(true);
const useNumbers = ref(true);
const useSymbols = ref(true);
const generatedPassword = ref('');

const generatePassword = () => {
  const lowercase = 'abcdefghijklmnopqrstuvwxyz';
  const uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
  const numbers = '0123456789';
  const symbols = '!@#$%^&*()-_=+[]{}<>?';

  let chars = lowercase;
  if (useUppercase.value) chars += uppercase;
  if (useNumbers.value) chars += numbers;
  if (useSymbols.value) chars += symbols;

  let pwd = '';
  for (let i = 0; i < genLength.value; i++) {
    const randIndex = Math.floor(Math.random() * chars.length);
    pwd += chars.charAt(randIndex);
  }

  generatedPassword.value = pwd;
};

const copyToClipboard = (text: string) => {
  navigator.clipboard
    .writeText(text)
    .then(() => $q.notify({ type: 'positive', message: t('copied') }))
    .catch(() => $q.notify({ type: 'negative', message: t('copyError') }));
};

const currentLang = ref<'fr' | 'en'>('en');
const toggleLang = () => {
  currentLang.value = currentLang.value === 'fr' ? 'en' : 'fr';
};

const translations = {
  fr: {
    title: 'Vérificateur de mot de passe',
    description: 'Vérifie la solidité, la sécurité et la confidentialité de ton mot de passe',
    enterPassword: 'Entrez votre mot de passe',
    minChar: 'Minimum 3 caractères',
    passwordStrengthIndicator: 'Indicateur de force du mot de passe',
    strength: 'Force',
    checkingLeaks: 'Vérification des fuites en cours...',
    foundInLeaks: ({ count }: { count: number }) =>
      `Ce mot de passe a été vu ${count} fois dans des fuites de données.`,
    notFoundInLeaks: "Ce mot de passe n'a pas été trouvé dans les fuites connues.",
    passwordGenerator: 'Générateur de mot de passe',
    passwordLength: 'Longueur du mot de passe',
    uppercase: 'Majuscules',
    numbers: 'Chiffres',
    symbols: 'Symboles',
    generatedPassword: 'Mot de passe généré',
    generate: 'Générer',
    copy: 'Copier',
    copied: 'Copié dans le presse-papiers ✅',
    copyError: 'Erreur lors de la copie 😓',
    darkMode: 'Mode sombre',
    showPassword: 'Afficher le mot de passe',
    hidePassword: 'Masquer le mot de passe',
  },
  en: {
    title: 'Password checker',
    description: 'Check the strength, security and privacy of your password',
    enterPassword: 'Enter your password',
    minChar: 'Minimum 3 characters',
    passwordStrengthIndicator: 'Password strength indicator',
    strength: 'Strength',
    checkingLeaks: 'Checking for breaches...',
    foundInLeaks: ({ count }: { count: number }) =>
      `This password has appeared ${count} times in data breaches.`,
    notFoundInLeaks: 'This password has not been found in any known breaches.',
    passwordGenerator: 'Password generator',
    passwordLength: 'Password length',
    uppercase: 'Uppercase',
    numbers: 'Numbers',
    symbols: 'Symbols',
    generatedPassword: 'Generated password',
    generate: 'Generate',
    copy: 'Copy',
    copied: 'Copied to clipboard ✅',
    copyError: 'Failed to copy 😓',
    darkMode: 'Dark mode',
    showPassword: 'Show password',
    hidePassword: 'Hide password',
  },
};

const t = (key: string, params?: { count?: number }): string => {
  const lang = translations[currentLang.value];
  const value = lang[key as keyof typeof lang];
  return typeof value === 'function' ? value({ count: 0, ...params }) : value;
};

const translatedSuggestions = computed(() => {
  if (!password.value) return [];
  const customSuggestionsFr = [
    'Utilisez au moins 12 caractères avec des majuscules, minuscules, chiffres et symboles.',
    'Évitez d’utiliser des informations personnelles comme votre prénom ou date de naissance.',
    'N’utilisez pas de mots trop simples ou des suites de clavier (ex. "azerty").',
    'Utilisez un mot de passe différent pour chaque service important.',
  ];

  const customSuggestionsEn = [
    'Use at least 12 characters including uppercase, lowercase, numbers, and symbols.',
    'Avoid using personal information such as your name or birth date.',
    'Do not use simple words or keyboard patterns like "qwerty".',
    'Use a different password for each important service.',
  ];

  return currentLang.value === 'fr' ? customSuggestionsFr : customSuggestionsEn;
});
</script>
