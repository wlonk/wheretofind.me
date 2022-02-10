import { mount } from '@vue/test-utils';
import AliasForm from '@/components/AliasForm.vue';
import MockUrls from '../mockUrls';

jest.mock('axios');
window.Urls = MockUrls;

describe('AliasForm.vue', () => {
  const setup = (options) => {
    const aliases = [
      {
        id: 1,
        name: 'Test 1',
      },
      {
        id: 2,
        name: 'Test 2',
      },
    ];
    const userInSearch = false;
    const mockGet = (url) =>
      url.indexOf('profile') !== -1
        ? Promise.resolve({ data: { search_enabled: false } })
        : Promise.resolve({ data: aliases });
    const $http = {
      post: jest.fn().mockResolvedValue({
        data: {
          id: 3,
          name: '',
        },
      }),
      patch: jest.fn().mockResolvedValue(Promise.resolve()),
      get: jest.fn(mockGet),
      delete: jest.fn().mockResolvedValue(Promise.resolve()),
    };
    const mocks = {
      $http,
    };
    const data = {
      aliases,
      userInSearch,
      draggingInProgress: false,
      runningRequests: 0,
    };
    const mountOptions = {
      mocks,
      data: () => data,
      ...options,
    };
    const wrapper = mount(AliasForm, mountOptions);
    return {
      $http,
      mocks,
      wrapper,
      data,
    };
  };

  test('reorder', () => {
    const { data, $http, wrapper } = setup();
    wrapper.setData(data);
    wrapper.vm.reorder();

    expect($http.post).toBeCalledWith('/api/aliases/reorder/', [1, 2]);
  });

  test('create/NewAlias', async () => {
    const { data, $http, wrapper } = setup();
    wrapper.setData(data);
    await wrapper.vm.create();
    expect($http.post).toBeCalledWith('/api/aliases/', {
      name: '',
    });
    await wrapper.vm.$nextTick();
    expect(wrapper.vm.aliases).toContainEqual({
      id: 3,
      name: '',
    });
  });

  test('changeUserSearchStatus', async () => {
    const { data, $http, wrapper } = setup();
    wrapper.setData({ userInSearch: true, aliases: data.aliases });
    await wrapper.vm.changeUserSearchStatus();
    expect($http.patch).toBeCalledWith('/api/profile/', {
      search_enabled: true,
    });
  });

  test('destroy/destroyAlias', async () => {
    const { data, $http, wrapper } = setup();
    wrapper.setData(data);
    await wrapper.vm.destroy(data.aliases[0]);
    expect($http.delete).toBeCalledWith('/api/aliases/1/');
    await wrapper.vm.$nextTick();
    expect(wrapper.vm.aliases).not.toContainEqual({
      id: 1,
      name: 'Test 1',
    });
  });

  test('retrieveAliases', () => {
    const { data, $http, wrapper } = setup();
    wrapper.vm.retrieveAliases(data.aliases[0]);

    expect($http.get).toBeCalledWith('/api/aliases/');
  });
});
