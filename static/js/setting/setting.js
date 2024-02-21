/*
Purpose:
   Settings
   Client side functionality for settings management

Contributors:
   Michael Gurewitz
   
*/

const axios = window.axios;

async function updateSetting(settingId, settingValue) {
    try {
      const response = await axios.post(`/api/settings/${settingId}`, { 
        settingValue 
      });
      console.log(response.data);
      } catch (error) {
      console.error(error);
    }
}

document.addEventListener('DOMContentLoaded', (event) => {
  const updateSettingForm = document.getElementById('updateSettingForm');
  if (updateSettingForm) {
    updateSettingForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const formData = new FormData(updateSettingForm);
      const settingId = formData.get('settingId');
      const settingValue = formData.get('settingValue');
      await updateSetting(settingId, settingValue);
    });
  }
});