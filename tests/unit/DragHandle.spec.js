import { mount } from '@vue/test-utils';
import Alias from '@/components/Alias.vue';

describe('DragHandle.vue', () => {
  const setup = options => {
    const mountOptions = {
      ...options,
      propsData: {
        alias: {
          id: 1,
          name: 'Test Alias',
        },
        disabled: false,
        index: 0,
      },
    };
    const wrapper = mount(Alias, mountOptions);
    return {
      wrapper,
    };
  };

  test('up', async () => {
    const { wrapper } = setup();
    const event = {
      keyCode: 38,
    };
    wrapper.find('.rearrange-handle').trigger('keydown', event);
    await wrapper.vm.$nextTick(); // Wait until $emits have been handled
    expect(wrapper.emitted().moved).toBeTruthy();
  });

  test('down', async () => {
    const { wrapper } = setup();
    const event = {
      keyCode: 40,
    };
    wrapper.find('.rearrange-handle').trigger('keydown', event);
    await wrapper.vm.$nextTick(); // Wait until $emits have been handled
    expect(wrapper.emitted().moved).toBeTruthy();
  });
});
