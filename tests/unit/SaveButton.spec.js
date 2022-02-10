import { shallowMount } from '@vue/test-utils';
import SaveButton from '@/components/SaveButton.vue';

describe('SaveButton.vue', () => {
  const generateWrapper = () => {
    const propsData = {
      allRequestsComplete: true,
    };
    const wrapper = shallowMount(SaveButton, { propsData });
    return wrapper;
  };

  test('Goes into spinnning mode after click and stops after 400ms (unless already spinning because !allRequestsComplete)', async () => {
    const wrapper = generateWrapper();
    jest.useFakeTimers();

    wrapper.find('button').trigger('click');
    expect(wrapper.vm.animatingDueToClick).toBe(true);
    expect(wrapper.vm.spinning).toBe(true);

    jest.advanceTimersByTime(401);
    expect(wrapper.vm.animatingDueToClick).toBe(false);
    expect(wrapper.vm.spinning).toBe(false);

    await wrapper.setProps({ allRequestsComplete: false });
    expect(wrapper.vm.spinning).toBe(true);

    wrapper.find('button').trigger('click');
    expect(wrapper.vm.animatingDueToClick).toBe(false);
  });

  test('Goes into spinning mode when !allRequestsComplete', async () => {
    const wrapper = generateWrapper();
    await wrapper.setProps({ allRequestsComplete: false });
    expect(wrapper.vm.spinning).toBe(true);
    await wrapper.setProps({ allRequestsComplete: true });
    expect(wrapper.vm.spinning).toBe(false);
  });

  test('Button is disabled when !allRequestsComplete', async () => {
    const wrapper = generateWrapper();
    await wrapper.setProps({ allRequestsComplete: false });
    const button = wrapper.find('button');
    await wrapper.vm.$nextTick();
    expect(button.element.disabled).toBe(true);
  });

  test('Do nothing if not allRequestsComplete', async () => {
    const wrapper = generateWrapper();
    await wrapper.setProps({ allRequestsComplete: false });
    wrapper.vm.showSaveAnimation();
    expect(wrapper.vm.animatingDueToClick).toBe(false);
  });
});
