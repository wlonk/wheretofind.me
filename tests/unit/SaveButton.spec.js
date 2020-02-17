import { shallowMount } from '@vue/test-utils';
import SaveButton from '@/components/SaveButton.vue';

describe('SaveButton.vue', () => {
  const propsData = {
    allUploadsComplete: true,
  };
  const wrapper = shallowMount(SaveButton, { propsData });
  test('Goes into spinnning mode after click and stops after 400ms (unless already spinning because !allUploadsComplete)', () => {
    jest.useFakeTimers();
    wrapper.find('button').trigger('click');
    expect(wrapper.vm.animatingDueToClick).toBe(true);
    expect(wrapper.vm.spinning).toBe(true);
    jest.advanceTimersByTime(401);
    expect(wrapper.vm.animatingDueToClick).toBe(false);
    expect(wrapper.vm.spinning).toBe(false);
    wrapper.setProps({ allUploadsComplete: false });
    expect(wrapper.vm.spinning).toBe(true);
    wrapper.find('button').trigger('click');
    expect(wrapper.vm.animatingDueToClick).toBe(false);
  });
  test('Goes into spinning mode when !allUploadsComplete', () => {
    wrapper.setProps({ allUploadsComplete: false });
    expect(wrapper.vm.spinning).toBe(true);
    wrapper.setProps({ allUploadsComplete: true });
    expect(wrapper.vm.spinning).toBe(false);
  });
  test('Button is disabled when !allUploadsComplete', async () => {
    wrapper.setProps({ allUploadsComplete: false });
    const button = wrapper.find('button');
    await wrapper.vm.$nextTick();
    expect(button.element.disabled).toBe(true);
  });
});
