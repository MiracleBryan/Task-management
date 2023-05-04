<template>
  <q-layout view="hHh lpR fFf" class="main_layout bg-indigo-1">

    <!-- Main Header -->
    <q-header class="main_header bg-indigo-1 text-grey-9">
      <q-toolbar style="padding: 0">
        <q-toolbar-title class="q-mx-md-lg q-my-xs-sm q-my-md-md">
          <div class="flex row justify-between">

            <!-- Logo & Brand Name -->
            <div class="flex row items-center">
              <!-- Logo -->
              <q-avatar class="q-mx-sm cursor-pointer" style="opacity: 0.75;">
                <img src="https://cdn.quasar.dev/logo-v2/svg/logo-mono-black.svg" class="logo">
              </q-avatar>

              <!-- Brand Name -->
              <div class="flex no-pointer-events">
                <h5 class="brand_name_main text-weight-bold" style="margin: 0; margin-left: 0.25em">arjoma</h5>
                <span class="brand_name_desc" style="padding-top: 0.05em; padding-left: 0.35em"> task management</span>
              </div>
            </div>

            <!-- Control Buttons -->
            <div>
              <!-- Drawer Button -->
              <q-btn class="menu_button" unelevated @click="right_drawer_open = !right_drawer_open" round color="indigo-5"
                icon="menu">
                <q-tooltip :delay="350" anchor="bottom middle" self="top middle" :offset="[10, 5]" transition-show="scale"
                  transition-hide="scale">
                  Menu
                </q-tooltip>
              </q-btn>

              <!-- Account Button -->
              <q-btn unelevated outline round class="profile_avatar q-mr-md q-ml-sm" @click="show_account_tip = false">
                <!-- Profile Image -->
                <q-avatar size="45px" class="toolbar_profile_avatar">
                  <img v-if="user.picture" :src="image_url" />
                  <q-icon v-else color="grey-8" size="45px" name="face" />

                  <!-- Account Button Expansion (darkmode, logout) -->
                  <q-menu>
                    <div class="flex column q-px-md q-py-md">
                      <!-- Route Back To Profile -->
                      <q-btn align="left" flat class="account_profile_button q-mb-sm" @click="go_to_profile"
                        v-close-popup>
                        <div class="flex row no-wrap items-center">
                          <!-- Profile Image -->
                          <q-avatar size="40px" class="toolbar_profile_avatar q-mr-sm">
                            <img v-if="user.picture" :src="image_url" />
                            <q-icon v-else color="grey-8" size="40px" name="face" />
                          </q-avatar>
                          <span class="q-pt-xs" style="overflow:hidden; white-space:nowrap">{{ user.name }}</span>
                        </div>
                      </q-btn>

                      <!-- Dark Mode Toggle -->
                      <q-toggle v-model="dark" :dark="dark" color="cyan-10" size="md" checked-icon="nights_stay"
                        unchecked-icon="light_mode" class="dark_mode_toggle q-mr-lg q-mb-lg text-grey-7"
                        label="Dark Mode">
                      </q-toggle>

                      <!-- Logout -->
                      <q-btn class="logout_btn bg-indigo-5 text-white" @click="logout" no-caps>Logout</q-btn>
                    </div>
                  </q-menu>

                  <!-- Tooltip -->
                  <q-tooltip :delay="350" v-model="show_account_tip" anchor="bottom middle" self="top middle"
                    :offset="[10, 5]" transition-show="scale" transition-hide="scale">
                    Account
                  </q-tooltip>
                </q-avatar>
              </q-btn>
            </div>
          </div>
        </q-toolbar-title>
      </q-toolbar>
    </q-header>

    <!-- Drawer -->
    <q-drawer class="drawer" :width="260" v-model="right_drawer_open" side="right">
      <!-- Chevron Expander : Removed for now. -->
      <!-- <div class="drawer_slider text-grey-7" @click="right_drawer_open = !right_drawer_open"
        :class="{ shrink_slider: !right_drawer_open, expand_slider: right_drawer_open }">
        <q-icon name="chevron_right" size="1.6em" style="padding: 6px 3px"></q-icon>
      </div> -->

      <!-- Drawer Components -->
      <template v-if="viewing_user">
        <ProfileComponent></ProfileComponent>

        <q-separator></q-separator>

        <div class="drawer_utility flex column items-center">

          <!-- Workload -->
          <div>
            <q-btn no-caps class="text-grey-8 q-mt-md" style="width:190px" align="left" flat
              @click="this.$refs.busy.show_busyness()">
              <q-icon name="hourglass_full" class="q-pr-md" />Workload
            </q-btn>
            <BusynessComponent ref="busy" :user_id="viewing_user.id" :is_dark="dark" />
          </div>

          <!-- Task History -->
          <div>
            <q-btn no-caps class="text-grey-8 q-mt-md" style="width:190px" align="left" flat
              @click="this.$refs.history.show_history()">
              <q-icon name="work_history" class="q-pr-md" />Task History
            </q-btn>
            <TaskHistory ref="history" :user_id="viewing_user.id" :is_dark="dark" />
          </div>

          <template v-if="!readonly">
            <!-- Connection List -->
            <div>
              <q-btn no-caps class="text-grey-8 q-mt-sm" style="width:190px" align="left" flat
                :class="[expand_connection ? 'connection_expanded' : '']" @click="expand_connection = !expand_connection">
                <q-icon name="people" class="q-pr-md" />Connections
              </q-btn>

              <transition appear enter-active-class="animated fadeIn" leave-active-class="animated fadeOut">
                <ConnectionList v-show="expand_connection"></ConnectionList>
              </transition>
            </div>

            <!-- Adding People -->
            <div>
              <q-btn no-caps class="text-grey-8 q-mt-sm" style="width:190px" align="left" flat
                @click="this.$refs.conn_prompt.show_add_dialog()">
                <q-icon name="person_add" class="q-pr-md" />Add People
              </q-btn>
              <ConnectionRequestPrompt ref="conn_prompt" />
            </div>
          </template>

        </div>
      </template>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>

  </q-layout>
</template>

<script>
import ConnectionList from 'src/components/connection/ConnectionList.vue'
import ConnectionRequestPrompt from 'src/components/connection/ConnectionRequestPrompt.vue'
import ProfileComponent from 'src/components/profile/ProfileComponent.vue'
import BusynessComponent from 'src/components/busyness/BusynessComponent.vue'
import TaskHistory from 'src/components/task_history/TaskHistory.vue'
import AuthAPI from 'src/services/user.api.js'
import { useAppStore } from 'src/stores/AppStore'
import { get_access_token_attr_key, get_dark_mode_attr_key } from 'src/utils/local_storage_utils'
import { Dark } from 'quasar'
import { get_base_url } from 'src/services/utils.js'

export default {
  components: {
    ConnectionList,
    ProfileComponent,
    ConnectionRequestPrompt,
    BusynessComponent,
    TaskHistory
  },
  data() {
    return {
      right_drawer_open: false,
      expand_connection: false,
      dark: false,
      show_account_tip: false,
    }
  },
  created() {
    // Initialize Dark Mode.
    this.dark = Boolean(parseInt(localStorage.getItem(get_dark_mode_attr_key())))

    // Auto open drawer on desktop. Probably use the breakpoint in Quasar...
    if (window.innerWidth >= 600) {
      this.right_drawer_open = true
    }
  },
  watch: {
    dark(new_value, old_value) {
      Dark.set(new_value)

      // Persist mode to local storage.
      localStorage.setItem(get_dark_mode_attr_key(), new_value ? 1 : 0)
    }
  },
  computed: {
    // The query user
    viewing_user() {
      return useAppStore().viewing_user
    },

    // The user
    user() {
      return useAppStore().user
    },

    readonly() {
      return useAppStore().user_readonly
    },

    image_url() {
      return `${get_base_url()}/${this.user.picture}`
    },
  },
  methods: {
    // Go to user's profile / task list.
    go_to_profile() {
      this.$router.push({ path: '/tasks', query: { user: this.user.id } })
    },

    // Logout the user.
    logout() {
      AuthAPI.logout()
      localStorage.removeItem(get_access_token_attr_key())
      this.$router.go()
    }
  }
}
</script>

<style lang="scss">
.main_layout {
  transition: background-color 0.35s ease;
}

.main_header {
  transition: background-color 0.35s ease;
}

.logo {
  transition: all 1s ease;
}

.q-drawer {
  transition: background-color 0.35s ease;
}

.drawer {
  transition: background-color 0.35s ease;
}

// Dark Mode
.body--dark {
  .main_layout {
    background-color: $dark !important;
  }

  .main_header {
    background-color: $dark !important;
    color: $grey-4 !important;
  }

  .menu_button {
    background-color: $dark-bg-fill-4 !important;
  }

  .logo {
    filter: saturate(270%) hue-rotate(13deg) brightness(1500%);
    transform: rotate(30deg) scale(0.95);
  }

  .logout_btn {
    background-color: $dark-bg-fill-2 !important;
  }

  .toolbar_profile_avatar i {
    color: $grey-3 !important;
  }

  .dark_mode_toggle {
    color: $grey-2 !important;
  }

  // Drawer
  .q-drawer {
    background-color: $dark-2;
  }

  .drawer {
    border-left: 1px solid $dark-bg-fill-2;
    border-top: 1px solid $dark-bg-fill-2;
    border-top-left-radius: 9px;
  }

  // Drawer Slider
  .drawer_slider {
    background-color: $dark-bg-fill-1;
    color: $grey-5 !important;
  }

  .drawer_slider:hover {
    background-color: $dark-bg-fill-3;
  }

  // Drawer Utility Buttons
  .drawer_utility {
    .q-btn {
      color: $grey-5 !important;

      &:hover {
        color: $grey-1 !important;
      }
    }
  }

  // Connection list button (Expanded)
  .connection_expanded {
    background-color: $dark-bg-fill-1 !important;
  }

  // Menu Styles
  .q-menu {
    .q-field__control {
      color: $lime-11;
    }
  }
}

// Light Mode
.body--light {

  // Logo
  .logo {
    transform: rotate(-30deg);
  }

  // Drawer Slider
  .drawer_slider {
    background-color: #f6f7fb;
    color: $grey-8 !important;
  }

  .drawer_slider:hover {
    background-color: #dcdfec;
  }
}

// Drawer Slider
.drawer_slider {
  cursor: pointer;
  width: 28px;
  height: 35px;
  border-radius: 11px 0px 11px 0px;
  position: absolute;
  z-index: 1;
}

.shrink_slider {
  transform: translateX(-26px) rotate(180deg);
  border-radius: 0px 9px 9px 0px;
  transition: transform 0.2s ease, background-color 0.35s ease;
}

.expand_slider {
  transform: translateX(0) rotate(0deg);
  border-radius: 9px 0px 9px 0px;
  transition: transform 0.1s ease, background-color 0.35s ease;
}

.q-drawer {
  border-top-left-radius: 11px;
}

.q-layout--prevent-focus {
  visibility: visible !important;
}

// Connection list button (Expanded)
.connection_expanded {
  background-color: $grey-3 !important;
}

// Responsiveness
@media (max-width: 600px) {
  .brand_name_desc {
    display: none
  }
}
</style>