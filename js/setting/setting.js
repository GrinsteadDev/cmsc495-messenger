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