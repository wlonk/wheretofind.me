import { shallowMount } from '@vue/test-utils';
import FavStar from '@/components/FavStar.vue';
import MockUrls from '../mockUrls';

jest.mock('axios');
window.Urls = MockUrls;

describe('FavStar.vue', () => {
  const setup = options => {
    const $http = {
      post: jest.fn(),
      patch: jest.fn(),
      delete: jest.fn(),
    };
    const mocks = {
      $http,
    };
    const propsData = {
      username: 'test',
      small: false,
      ...options.propsData,
    };
    const mountOptions = {
      propsData,
      mocks,
    };
    const wrapper = shallowMount(FavStar, mountOptions);
    return {
      wrapper,
      $http,
      mocks,
      propsData,
    };
  };

  test('toggleFavstar restores inactive if follow fails', () => {
    const options = { propsData: { active: false } };
    const { wrapper } = setup(options);
    wrapper.vm.follow = jest.fn().mockReturnValue(Promise.reject());

    wrapper.vm.toggleFavstar();
    expect(wrapper.vm.follow).toHaveBeenCalled();
    expect(wrapper.vm.active).toBe(false);
  });

  test('toggleFavstar restores active if unfollow fails', () => {
    const options = { propsData: { active: true } };
    const { wrapper } = setup(options);
    wrapper.vm.unfollow = jest.fn().mockReturnValue(Promise.reject());

    wrapper.vm.toggleFavstar();
    expect(wrapper.vm.unfollow).toHaveBeenCalled();
    expect(wrapper.vm.active).toBe(true);
  });

  test('unfollow', () => {
    const options = { propsData: { active: true } };
    const { wrapper } = setup(options);

    wrapper.vm.unfollow();
    expect(wrapper.vm.$http.delete).toHaveBeenCalledWith('/api/follows/test/');
  });

  test('follow', () => {
    const options = { propsData: { active: false } };
    const { wrapper } = setup(options);

    wrapper.vm.follow();
    expect(wrapper.vm.$http.post).toHaveBeenCalledWith('/api/follows/', {
      to_user: 'test',
      nickname: '',
    });
  });

  test('showNickname', () => {
    const options = { propsData: { active: true } };
    const { wrapper } = setup(options);

    wrapper.vm.toggleShowNickname().then(() => {
      expect(wrapper.vm.showNicknameField).toBeTruthy();
    });
  });

  test('updateNickname', () => {
    const options = { propsData: { active: true } };
    const { wrapper } = setup(options);

    wrapper.vm.updateNickname();
    expect(wrapper.vm.$http.patch).toHaveBeenCalledWith('/api/follows/test/', {
      nickname: '',
    });
    expect(wrapper.vm.showNicknameField).toBeFalsy();
  });
});
