import { shallowMount } from '@vue/test-utils';
import SaveButton from '@/components/SaveButton.vue';

describe('SaveButton.vue', () => {
  const propsData = {
    allRequestsComplete: true,
  };
  const wrapper = shallowMount(SaveButton, { propsData });
  test('Goes into spinnning mode after click and stops after 400ms (unless already spinning because !allRequestsComplete)', () => {
    jest.useFakeTimers();
    wrapper.find('button').trigger('click');
    expect(wrapper.vm.animatingDueToClick).toBe(true);
    expect(wrapper.vm.spinning).toBe(true);
    jest.advanceTimersByTime(401);
    expect(wrapper.vm.animatingDueToClick).toBe(false);
    expect(wrapper.vm.spinning).toBe(false);
    wrapper.setProps({ allRequestsComplete: false });
    expect(wrapper.vm.spinning).toBe(true);
    wrapper.find('button').trigger('click');
    expect(wrapper.vm.animatingDueToClick).toBe(false);
  });
  test('Goes into spinning mode when !allRequestsComplete', () => {
    wrapper.setProps({ allRequestsComplete: false });
    expect(wrapper.vm.spinning).toBe(true);
    wrapper.setProps({ allRequestsComplete: true });
    expect(wrapper.vm.spinning).toBe(false);
  });
  test('Button is disabled when !allRequestsComplete', async () => {
    wrapper.setProps({ allRequestsComplete: false });
    const button = wrapper.find('button');
    await wrapper.vm.$nextTick();
    expect(button.element.disabled).toBe(true);
  });
});
